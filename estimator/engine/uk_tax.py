"""UK income tax and employer National Insurance (pure functions, no Django)."""

from decimal import Decimal as D

from ..data import uk_rates as r

ZERO = D("0")


def personal_allowance(income: D) -> D:
    """Allowance after the taper: £1 lost for every £2 of income over £100,000."""
    if income <= r.TAPER_THRESHOLD:
        return r.PERSONAL_ALLOWANCE
    reduction = (income - r.TAPER_THRESHOLD) * r.TAPER_RATE
    return max(ZERO, r.PERSONAL_ALLOWANCE - reduction)


def income_tax(income: D) -> D:
    """Total UK income tax on `income`. This is the UKTax() in T = UKTax(I + T)."""
    income = max(ZERO, income)
    taxable = max(ZERO, income - personal_allowance(income))

    basic_part = min(taxable, r.BASIC_BAND_WIDTH)
    higher_part = min(
        max(ZERO, taxable - r.BASIC_BAND_WIDTH),
        r.ADDITIONAL_THRESHOLD - r.BASIC_BAND_WIDTH,
    )
    additional_part = max(ZERO, taxable - r.ADDITIONAL_THRESHOLD)

    return (
        basic_part * r.BASIC_RATE
        + higher_part * r.HIGHER_RATE
        + additional_part * r.ADDITIONAL_RATE
    )


def employer_national_insurance(pay: D) -> D:
    """Employer Class 1 NI on pay above the secondary threshold."""
    return max(ZERO, pay - r.EMPLOYER_NI_SECONDARY_THRESHOLD) * r.EMPLOYER_NI_RATE
