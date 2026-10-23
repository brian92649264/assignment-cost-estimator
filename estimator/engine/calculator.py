from dataclasses import dataclass, field
from decimal import Decimal as D
from types import ModuleType

from ..data import swiss_rates, uk_benefits, uk_rates
from . import swiss as swiss_module
from . import uk_tax
from .grossup import GrossUpResult, gross_up

CASH = "cash"
BIK = "bik"
EXEMPT = "exempt"
REMOVAL = "removal"
TREATMENT_LABELS = {
    CASH: "Taxable cash",
    BIK: "Taxable benefit in kind",
    EXEMPT: "Not taxable in the UK",
    REMOVAL: "Removal cost (first £8,000 not taxed)",
}
TAXABLE_TREATMENTS = {CASH, BIK}


@dataclass(frozen=True)
class Benefit:
    label: str
    amount_gbp: D  
    treatment: str  
    year_one_only: bool = False
    note: str = ""


@dataclass(frozen=True)
class AssignmentInputs:
    salary_chf: D
    bonus_chf: D
    years: int
    chf_per_gbp: D  
    benefits: list[Benefit]


@dataclass(frozen=True)
class Line:
    label: str
    amount_gbp: D 
    note: str = ""
    treatment: str = ""  


@dataclass(frozen=True)
class Section:
    title: str
    lines: list[Line]
    reduces_cost: bool = False

    @property
    def total(self) -> D:
        return sum((line.amount_gbp for line in self.lines), D("0"))


@dataclass(frozen=True)
class YearResult:
    year_number: int
    sections: list[Section]
    home_pay: D
    employer_cost: D
    gross_up: GrossUpResult

    @property
    def multiple_of_home_pay(self) -> D:
        return self.employer_cost / self.home_pay


@dataclass(frozen=True)
class AssignmentResult:
    years: list[YearResult]
    assumptions: list[str] = field(default_factory=list)

    @property
    def total_cost(self) -> D:
        return sum((y.employer_cost for y in self.years), D("0"))

    @property
    def total_home_pay(self) -> D:
        return sum((y.home_pay for y in self.years), D("0"))

    @property
    def multiple_of_home_pay(self) -> D:
        return self.total_cost / self.total_home_pay


def calculate(
    inputs: AssignmentInputs, swiss: ModuleType = swiss_module
) -> AssignmentResult:
    removal_left = uk_benefits.REMOVAL_EXEMPTION_LIMIT
    years = []
    for n in range(1, inputs.years + 1):
        year, removal_left = _calculate_year(n, inputs, swiss, removal_left)
        years.append(year)
    return AssignmentResult(years=years, assumptions=_assumptions(inputs))


def _benefit_lines(active: list[Benefit], removal_left: D) -> tuple[list[Line], D, D]:
    lines: list[Line] = []
    taxable = D("0")
    for b in active:
        note = b.note
        if b.treatment == REMOVAL:
            exempt_part = min(b.amount_gbp, removal_left)
            taxed_part = b.amount_gbp - exempt_part
            removal_left -= exempt_part
            taxable += taxed_part
            limit = f"£{uk_benefits.REMOVAL_EXEMPTION_LIMIT:,.0f}"
            if taxed_part > 0:
                note = (
                    f"£{exempt_part:,.0f} is within the {limit} removal limit; "
                    f"£{taxed_part:,.0f} is above it and taxed."
                )
            else:
                note = f"Within the {limit} removal limit. {b.note}".strip()
        elif b.treatment in TAXABLE_TREATMENTS:
            taxable += b.amount_gbp
        lines.append(
            Line(b.label, b.amount_gbp, note, treatment=TREATMENT_LABELS[b.treatment])
        )
    return lines, taxable, removal_left


def _calculate_year(
    year_number: int,
    inputs: AssignmentInputs,
    swiss: ModuleType,
    removal_left: D,
) -> tuple[YearResult, D]:
    fx = inputs.chf_per_gbp

    salary = inputs.salary_chf / fx
    bonus = inputs.bonus_chf / fx
    home_pay = salary + bonus
    home_section = Section(
        "1. Home pay",
        [
            Line("Base salary", salary, f"CHF {inputs.salary_chf:,.0f} at {fx}"),
            Line("Bonus", bonus, f"CHF {inputs.bonus_chf:,.0f} at {fx}"),
        ],
    )


    active = [b for b in inputs.benefits if year_number == 1 or not b.year_one_only]
    benefit_lines, taxable_benefits, removal_left = _benefit_lines(active, removal_left)
    benefit_section = Section("2. Assignment benefits", benefit_lines)

    gross_chf = inputs.salary_chf + inputs.bonus_chf
    hypo_tax = swiss.hypothetical_income_tax_chf(gross_chf) / fx
    hypo_ss = swiss.hypothetical_social_security_chf(gross_chf) / fx

    initial_pay = (home_pay - hypo_tax - hypo_ss) + taxable_benefits
    grossed = gross_up(initial_pay, uk_tax.income_tax)

    host_lines = [
        Line(
            "UK income tax (including tax on tax)",
            grossed.tax,
            f"Solved by iteration in {grossed.iterations} steps",
        )
    ]
    if uk_rates.SOCIAL_SECURITY_SYSTEM == "UK":
        ni = uk_tax.employer_national_insurance(grossed.taxable_pay)
        host_lines.append(Line("Employer National Insurance", ni))
    else:
        host_lines.append(
            Line(
                "Employer National Insurance",
                D("0"),
                "Swiss social security continues to apply, so no UK NI",
            )
        )
    host_section = Section("3. Host tax and charges paid by the employer", host_lines)

    deductions_section = Section(
        "4. Deductions (hypothetical Swiss)",
        [
            Line("Hypothetical Swiss income tax", hypo_tax),
            Line("Hypothetical Swiss social security", hypo_ss),
        ],
        reduces_cost=True,
    )

    employer_cost = (
        home_section.total
        + benefit_section.total
        + host_section.total
        - deductions_section.total
    )
    result = YearResult(
        year_number=year_number,
        sections=[home_section, benefit_section, host_section, deductions_section],
        home_pay=home_pay,
        employer_cost=employer_cost,
        gross_up=grossed,
    )
    return result, removal_left


def _assumptions(inputs: AssignmentInputs) -> list[str]:
    return [
        f"UK {uk_rates.TAX_YEAR} rates are used for every year of the assignment.",
        "England income tax bands apply, because the employee works in London.",
        "No pension contributions or Gift Aid, so adjusted net income (used for "
        "the personal allowance taper) equals taxable pay.",
        f"Exchange rate fixed at £1 = CHF {inputs.chf_per_gbp} for all years.",
        "The employee is UK tax resident throughout and leaves Swiss tax residence.",
        "The UK subsidiary runs the payroll; the employer pays all UK income tax.",
        f"Social security system applied: {uk_rates.SOCIAL_SECURITY_SYSTEM}.",
        *uk_benefits.ASSUMPTIONS,
        *swiss_rates.ASSUMPTIONS,
    ]