"""Form validation. Bad input produces readable messages, never a crash."""

from decimal import Decimal as D

from django import forms

from .engine.calculator import (
    BIK,
    CASH,
    EXEMPT,
    TREATMENT_LABELS,
    AssignmentInputs,
    Benefit,
)

COUNTRIES_HOME = [("CH", "Switzerland (city of Zurich)")]
COUNTRIES_HOST = [("GB", "United Kingdom (London)")]
TREATMENT_CHOICES = [(k, v) for k, v in TREATMENT_LABELS.items()]

# Defaults are the test case from the assessment pack.
TEST_CASE_INITIAL = {
    "home_country": "CH",
    "host_country": "GB",
    "salary_chf": "150000",
    "bonus_chf": "20000",
    "years": 2,
    "chf_per_gbp": "1.10",
    "housing_monthly_gbp": "3000",
    "housing_treatment": BIK,
    "relocation_chf": "5000",
    "relocation_treatment": CASH,
    "moving_gbp": "6000",
    "moving_treatment": EXEMPT,
    "temp_housing_gbp": "4000",
    "temp_housing_treatment": EXEMPT,
}


def _money(label: str, help_text: str, required: bool = True) -> forms.DecimalField:
    return forms.DecimalField(
        label=label,
        help_text=help_text,
        required=required,
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


class AssignmentForm(forms.Form):
    home_country = forms.ChoiceField(
        label="Home country", choices=COUNTRIES_HOME,
        help_text="Where the employee is paid and taxed today.",
    )
    host_country = forms.ChoiceField(
        label="Host country", choices=COUNTRIES_HOST,
        help_text="Where the employee will work. The employer pays this country's tax.",
    )
    years = forms.TypedChoiceField(
        label="Assignment length",
        choices=[(1, "1 year"), (2, "2 years"), (3, "3 years")],
        coerce=int,
        help_text="Each assignment year is one UK tax year (6 April to 5 April).",
    )
    salary_chf = _money("Base salary (CHF a year)", "Annual home salary before any tax.")
    bonus_chf = _money("Bonus (CHF a year)", "Annual bonus. Enter 0 if there is none.")
    chf_per_gbp = forms.DecimalField(
        label="Exchange rate (CHF per £1)",
        help_text="For example 1.10 means £1 = CHF 1.10. Fixed for every year.",
        min_value=D("0.0001"),
        max_digits=8,
        decimal_places=4,
        error_messages={
            "required": "Enter an exchange rate, for example 1.10.",
            "invalid": "Exchange rate must be a number, for example 1.10.",
            "min_value": "Exchange rate must be greater than zero.",
        },
    )

    housing_monthly_gbp = _money(
        "Housing in the UK (£ a month)",
        "Rent the employer pays each month for the whole assignment.",
    )
    housing_treatment = forms.ChoiceField(label="Housing tax treatment", choices=TREATMENT_CHOICES)

    relocation_chf = _money("Relocation allowance", "One-off cash payment.")
    relocation_treatment = forms.ChoiceField(label="Relocation tax treatment", choices=TREATMENT_CHOICES)

    moving_gbp = _money("Moving costs (£, year 1 only)", "Flights and shipping paid by the employer.")
    moving_treatment = forms.ChoiceField(label="Moving costs tax treatment", choices=TREATMENT_CHOICES)

    temp_housing_gbp = _money("Temporary housing (£, year 1 only)", "For example a serviced apartment.")
    temp_housing_treatment = forms.ChoiceField(label="Temporary housing tax treatment", choices=TREATMENT_CHOICES)

    def to_inputs(self) -> AssignmentInputs:
        """Turn validated form data into the engine's input object."""
        d = self.cleaned_data
        fx = d["chf_per_gbp"]
        benefits = [
            Benefit("Housing in London", d["housing_monthly_gbp"] * 12, d["housing_treatment"]),
            Benefit("Relocation allowance", d["relocation_chf"] / fx, d["relocation_treatment"], True),
            Benefit("Moving costs", d["moving_gbp"], d["moving_treatment"], True),
            Benefit("Temporary housing", d["temp_housing_gbp"], d["temp_housing_treatment"], True),
        ]
        return AssignmentInputs(
            home_country=d["home_country"],
            host_country=d["host_country"],
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
