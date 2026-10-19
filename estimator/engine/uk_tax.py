"""UK income tax and employer National Insurance (pure functions, no Django)."""

from dataclasses import dataclass
from decimal import Decimal as D

from ..data import uk_rates as r

ZERO = D("0")


@dataclass(frozen=True)
class TaxDetail:
    """Income tax on one amount of income, with the working shown."""

    income: D
    personal_allowance: D
    taxable_income: D
    basic_tax: D
    higher_tax: D
    additional_tax: D

    @property
    def total(self) -> D:
        return self.basic_tax + self.higher_tax + self.additional_tax


def personal_allowance(income: D) -> D:
    """Allowance after the taper: £1 lost for every £2 of income over £100,000."""
    if income <= r.TAPER_THRESHOLD:
        return r.PERSONAL_ALLOWANCE
    reduction = (income - r.TAPER_THRESHOLD) * r.TAPER_RATE
    return max(ZERO, r.PERSONAL_ALLOWANCE - reduction)


def income_tax_detail(income: D) -> TaxDetail:
    income = max(ZERO, income)
    allowance = personal_allowance(income)
    taxable = max(ZERO, income - allowance)

    basic_part = min(taxable, r.BASIC_BAND_WIDTH)
    higher_part = min(
        max(ZERO, taxable - r.BASIC_BAND_WIDTH),
        r.ADDITIONAL_THRESHOLD - r.BASIC_BAND_WIDTH,
    )
    additional_part = max(ZERO, taxable - r.ADDITIONAL_THRESHOLD)

    return TaxDetail(
        income=income,
        personal_allowance=allowance,
        taxable_income=taxable,
        basic_tax=basic_part * r.BASIC_RATE,
        higher_tax=higher_part * r.HIGHER_RATE,
        additional_tax=additional_part * r.ADDITIONAL_RATE,
    )


def income_tax(income: D) -> D:
    """Total UK income tax on `income`. This is the UKTax() in T = UKTax(I + T)."""
    return income_tax_detail(income).total


def employer_national_insurance(pay: D) -> D:
    """Employer Class 1 NI on pay above the secondary threshold."""
    return max(ZERO, pay - r.EMPLOYER_NI_SECONDARY_THRESHOLD) * r.EMPLOYER_NI_RATE
