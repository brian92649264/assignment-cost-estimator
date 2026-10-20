"""Employer cost of an assignment, year by year.

Tax equalisation in one line: the employee keeps paying their usual home tax
(the hypothetical deductions), and the employer pays all the host tax.

Per year:
    home pay            salary + bonus, as if they had stayed in Switzerland
  + assignment benefits (housing, relocation, ...), each tagged by UK tax treatment
  + UK tax and charges  income tax incl. tax on tax, plus employer NI if it applies
  - hypothetical Swiss tax and social security
  = employer cost
"""

from dataclasses import dataclass, field
from decimal import Decimal as D
from types import ModuleType

from ..data import swiss_rates, uk_rates
from . import swiss as swiss_module
from . import uk_tax
from .grossup import GrossUpResult, gross_up

CASH = "cash"
BIK = "bik"
EXEMPT = "exempt"
TREATMENT_LABELS = {
    CASH: "Taxable cash",
    BIK: "Taxable benefit in kind",
    EXEMPT: "Not taxable in the UK",
}
TAXABLE_TREATMENTS = {CASH, BIK}


@dataclass(frozen=True)
class Benefit:
    label: str
    amount_gbp: D  # for the year it applies
    treatment: str  # CASH, BIK or EXEMPT
    year_one_only: bool = False


@dataclass(frozen=True)
class AssignmentInputs:
    home_country: str
    host_country: str
    salary_chf: D
    bonus_chf: D
    years: int
    chf_per_gbp: D  # £1 = CHF x
    benefits: list[Benefit]


@dataclass(frozen=True)
class Line:
    label: str
    amount_gbp: D  # always positive; the section decides if it adds or reduces cost
    note: str = ""
    treatment: str = ""  # tax treatment label for benefits


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
    """Run the full estimate. `swiss` is injectable so tests can use fixed rates."""
    fx = inputs.chf_per_gbp
    years = [_calculate_year(n, inputs, swiss, fx) for n in range(1, inputs.years + 1)]
    return AssignmentResult(years=years, assumptions=_assumptions(inputs))


def _calculate_year(
    year_number: int, inputs: AssignmentInputs, swiss: ModuleType, fx: D
) -> YearResult:
    # 1. Home pay
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

    # 2. Assignment benefits that apply this year
    active = [b for b in inputs.benefits if year_number == 1 or not b.year_one_only]
    benefit_section = Section(
        "2. Assignment benefits",
        [
            Line(b.label, b.amount_gbp, treatment=TREATMENT_LABELS[b.treatment])
            for b in active
        ],
    )
    taxable_benefits = sum(
        (b.amount_gbp for b in active if b.treatment in TAXABLE_TREATMENTS), D("0")
    )

    # 4 (computed early because it feeds the gross-up). Hypothetical deductions.
    gross_chf = inputs.salary_chf + inputs.bonus_chf
    hypo_tax = swiss.hypothetical_income_tax_chf(gross_chf) / fx
    hypo_ss = swiss.hypothetical_social_security_chf(gross_chf) / fx

    # 3. UK tax: gross up from I = net home pay + taxable benefits.
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
    return YearResult(
        year_number=year_number,
        sections=[home_section, benefit_section, host_section, deductions_section],
        home_pay=home_pay,
        employer_cost=employer_cost,
        gross_up=grossed,
    )


def _assumptions(inputs: AssignmentInputs) -> list[str]:
    # TODO(you): keep this list in step with the choices you actually make.
    return [
        f"UK {uk_rates.TAX_YEAR} rates are used for every year of the assignment.",
        f"Exchange rate fixed at £1 = CHF {inputs.chf_per_gbp} for all years.",
        "The employee is UK tax resident throughout and leaves Swiss tax residence.",
        "The UK subsidiary runs the payroll; the employer pays all UK income tax.",
        f"Social security system applied: {uk_rates.SOCIAL_SECURITY_SYSTEM}.",
        *swiss_rates.ASSUMPTIONS,
    ]