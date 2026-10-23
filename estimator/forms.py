"""Form validation. Bad input produces readable messages, never a crash."""

from decimal import Decimal as D

from django import forms

from .data import uk_benefits
from .engine.calculator import (
    CASH,
    REMOVAL,
    TREATMENT_LABELS,
    AssignmentInputs,
    Benefit,
)

COUNTRIES_HOME = [("CH", "Switzerland (city of Zurich)")]
COUNTRIES_HOST = [("GB", "United Kingdom (London)")]
YEAR_CHOICES = [(1, "1 year"), (2, "2 years"), (3, "3 years")]
TREATMENT_CHOICES = list(TREATMENT_LABELS.items())

# Defaults are the test case from the assessment pack.
TEST_CASE_INITIAL = {
    "home_country": "CH",
    "host_country": "GB",
    "salary_chf": "150000",
    "bonus_chf": "20000",
    "years": 2,
    "chf_per_gbp": "1.10",
    "housing_monthly_gbp": "3000",
    "housing_treatment": CASH,
    "relocation_chf": "5000",
    "relocation_treatment": CASH,
    "moving_gbp": "6000",
    "moving_treatment": REMOVAL,
    "temp_housing_gbp": "4000",
    "temp_housing_treatment": REMOVAL,
}


def _money(label: str) -> forms.DecimalField:
    """A non-negative amount of money, with readable error messages."""
    return forms.DecimalField(
        label=label,
        min_value=D("0"),
        max_digits=12,
        decimal_places=2,
        error_messages={
            "required": f"Enter a value for {label.lower()}.",
            "invalid": f"{label} must be a number, for example 150000.",
            "min_value": f"{label} cannot be negative.",
            "max_digits": f"{label} is too large.",
            "max_decimal_places": f"{label} can have at most 2 decimal places.",
        },
    )


def _treatment(label: str) -> forms.ChoiceField:
    """Dropdown for how the UK taxes a benefit."""
    return forms.ChoiceField(label=label, choices=TREATMENT_CHOICES)


class AssignmentForm(forms.Form):
    # The assignment
    home_country = forms.ChoiceField(label="Home country", choices=COUNTRIES_HOME)
    host_country = forms.ChoiceField(label="Host country", choices=COUNTRIES_HOST)
    years = forms.TypedChoiceField(
        label="Assignment length", choices=YEAR_CHOICES, coerce=int
    )
    salary_chf = _money("Base salary (CHF a year)")
    bonus_chf = _money("Bonus (CHF a year)")
    chf_per_gbp = forms.DecimalField(
        label="Exchange rate (CHF per £1)",
        min_value=D("0.0001"),
        max_digits=8,
        decimal_places=4,
        error_messages={
            "required": "Enter an exchange rate, for example 1.10.",
            "invalid": "Exchange rate must be a number, for example 1.10.",
            "min_value": "Exchange rate must be greater than zero.",
        },
    )

    # Assignment benefits: each is an amount plus its UK tax treatment.
    housing_monthly_gbp = _money("Housing in the UK (£ a month)")
    housing_treatment = _treatment("Housing tax treatment")

    relocation_chf = _money("Relocation allowance")
    relocation_treatment = _treatment("Relocation tax treatment")

    moving_gbp = _money("Moving costs (£, year 1 only)")
    moving_treatment = _treatment("Moving costs tax treatment")

    temp_housing_gbp = _money("Temporary housing (£, year 1 only)")
    temp_housing_treatment = _treatment("Temporary housing tax treatment")

    def to_inputs(self) -> AssignmentInputs:
        """Turn validated form data into the engine's input object."""
        d = self.cleaned_data
        fx = d["chf_per_gbp"]
        benefits = [
            Benefit(
                "Housing in London", d["housing_monthly_gbp"] * 12,
                d["housing_treatment"], note=uk_benefits.HOUSING_NOTE,
            ),
            Benefit(
                "Relocation allowance", d["relocation_chf"] / fx,
                d["relocation_treatment"], True, uk_benefits.RELOCATION_NOTE,
            ),
            Benefit(
                "Moving costs", d["moving_gbp"],
                d["moving_treatment"], True, uk_benefits.MOVING_NOTE,
            ),
            Benefit(
                "Temporary housing", d["temp_housing_gbp"],
                d["temp_housing_treatment"], True, uk_benefits.TEMP_HOUSING_NOTE,
            ),
        ]
        return AssignmentInputs(
            salary_chf=d["salary_chf"],
            bonus_chf=d["bonus_chf"],
            years=d["years"],
            chf_per_gbp=fx,
            benefits=benefits,
        )

    def clean(self):
        cleaned = super().clean()
        salary = cleaned.get("salary_chf")
        bonus = cleaned.get("bonus_chf")
        if salary is not None and bonus is not None and salary + bonus <= 0:
            raise forms.ValidationError("Salary and bonus cannot both be zero.")
        return cleaned