from decimal import Decimal as D

from ..data import uk_rates as r

ZERO = D("0")


def personal_allowance(income: D) -> D:
    if income <= r.TAPER_THRESHOLD:
        return r.PERSONAL_ALLOWANCE
    reduction = (income - r.TAPER_THRESHOLD) * r.TAPER_RATE
    return max(ZERO, r.PERSONAL_ALLOWANCE - reduction)


def income_tax(income: D) -> D:
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
    return max(ZERO, pay - r.EMPLOYER_NI_SECONDARY_THRESHOLD) * r.EMPLOYER_NI_RATE
