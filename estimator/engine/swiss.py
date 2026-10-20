"""Hypothetical Swiss tax and social security (CHF, pure functions, no Django).

Both are what the employee would have paid had they stayed in Zurich. The
employer deducts them from pay, which is why they reduce the employer's cost.

Method (checked against the ESTV tax calculator for a CHF 170,000 salary):
  net income    = gross - AHV/IV/EO - unemployment (ALV) - accident (NBU) - pension (BVG)
  taxable       = net income - professional expenses - insurance deduction
  federal tax   = tariff on taxable income (rounded down to CHF 100)
  Zurich tax    = basic tariff on taxable income (rounded down to CHF 100),
                  x 95% (canton) and x 119% (city), plus a flat personal tax
Each tax amount is rounded to the nearest whole franc, as the calculator does.

Hypothetical SOCIAL SECURITY is only AHV/IV/EO and ALV (BVG excluded, per the
brief). BVG and NBU appear here only because the calculator deducts them when
working out taxable income.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal as D

from ..data import swiss_rates as r

ZERO = D("0")


def _round_chf(amount: D) -> D:
    return amount.quantize(D("1"), rounding=ROUND_HALF_UP)


def _floor_to_100(amount: D) -> D:
    return (max(ZERO, amount) // 100) * 100


# --- Social security ----------------------------------------------------------
def ahv_iv_eo(gross: D) -> D:
    return gross * r.AHV_IV_EO_RATE


def alv(gross: D) -> D:
    return min(gross, r.ALV_SALARY_CEILING) * r.ALV_RATE


def hypothetical_social_security_chf(gross_chf: D) -> D:
    """AHV/IV/EO plus unemployment insurance. No BVG."""
    return ahv_iv_eo(gross_chf) + alv(gross_chf)


# --- Deductions the calculator makes before tax -------------------------------
def nbu(gross: D) -> D:
    return min(gross, r.NBU_SALARY_CEILING) * r.NBU_RATE


def bvg_employee(gross: D, age: int = r.EMPLOYEE_AGE) -> D:
    """Employee's half of the pension fund contribution."""
    if gross < r.BVG_ENTRY_THRESHOLD:
        return ZERO
    rate = next((rt for from_age, rt in r.BVG_RATE_FROM_AGE if age >= from_age), ZERO)
    mandatory_base = max(
        min(gross, r.BVG_UPPER_LIMIT) - r.BVG_COORDINATION_DEDUCTION,
        r.BVG_MIN_COORDINATED_SALARY,
    )
    extra_base = max(ZERO, gross - r.BVG_UPPER_LIMIT)
    total = mandatory_base * rate + extra_base * r.BVG_EXTRA_MANDATORY_RATE
    return total * r.BVG_EMPLOYEE_SHARE


def professional_expenses(net_income: D) -> D:
    flat = net_income * r.PROFESSIONAL_EXPENSES_RATE
    flat = min(max(flat, r.PROFESSIONAL_EXPENSES_MIN), r.PROFESSIONAL_EXPENSES_MAX)
    return min(flat, max(ZERO, net_income))


# --- Tax tariffs --------------------------------------------------------------
def zurich_basic_tax(taxable_income: D) -> D:
    """Einfache Staatssteuer: marginal bands, taxable income rounded down to 100."""
    remaining = _floor_to_100(taxable_income)
    tax = ZERO
    for width, rate in r.ZH_BASIC_TARIFF:
        part = remaining if width is None else min(remaining, width)
        tax += part * rate
        remaining -= part
        if remaining <= 0:
            break
    return tax


def federal_tax(taxable_income: D) -> D:
    income = _floor_to_100(taxable_income)
    if income < r.FEDERAL_TARIFF[0][0]:
        return ZERO
    if income >= r.FEDERAL_FLAT_FROM:
        tax = income * r.FEDERAL_FLAT_RATE
    else:
        start, base, per_100 = max(
            (row for row in r.FEDERAL_TARIFF if row[0] <= income), key=lambda row: row[0]
        )
        tax = base + (income - start) / 100 * per_100
    return ZERO if tax < r.FEDERAL_MIN_TAX else tax


# --- Putting it together ------------------------------------------------------
@dataclass(frozen=True)
class SwissTaxBreakdown:
    gross_chf: D
    ahv_iv_eo: D
    alv: D
    nbu: D
    bvg: D
    net_income: D
    professional_expenses: D
    taxable_income_canton: D
    taxable_income_federal: D
    basic_cantonal_tax: D
    cantonal_tax: D
    communal_tax: D
    personal_tax: D
    federal_tax: D

    @property
    def total_tax(self) -> D:
        return self.cantonal_tax + self.communal_tax + self.personal_tax + self.federal_tax


def hypothetical_tax_breakdown(gross_chf: D) -> SwissTaxBreakdown:
    ahv, unemployment = ahv_iv_eo(gross_chf), alv(gross_chf)
    accident, pension = nbu(gross_chf), bvg_employee(gross_chf)
    net = gross_chf - ahv - unemployment - accident - pension
    expenses = professional_expenses(net)

    taxable_canton = max(ZERO, net - expenses - r.INSURANCE_DEDUCTION_CANTON)
    taxable_federal = max(ZERO, net - expenses - r.INSURANCE_DEDUCTION_FEDERAL)

    basic = zurich_basic_tax(taxable_canton)
    return SwissTaxBreakdown(
        gross_chf=gross_chf,
        ahv_iv_eo=ahv,
        alv=unemployment,
        nbu=accident,
        bvg=pension,
        net_income=net,
        professional_expenses=expenses,
        taxable_income_canton=taxable_canton,
        taxable_income_federal=taxable_federal,
        basic_cantonal_tax=basic,
        cantonal_tax=_round_chf(basic * r.ZH_CANTON_MULTIPLIER),
        communal_tax=_round_chf(basic * r.ZH_CITY_MULTIPLIER),
        personal_tax=r.ZH_PERSONAL_TAX,
        federal_tax=_round_chf(federal_tax(taxable_federal)),
    )


def hypothetical_income_tax_chf(gross_chf: D) -> D:
    """Federal + cantonal + communal + personal tax on `gross_chf`."""
    return hypothetical_tax_breakdown(gross_chf).total_tax