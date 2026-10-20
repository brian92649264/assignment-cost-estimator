"""Swiss reference data for 2026 (CHF), with the page each rule came from.

Everything here is for a single employee living in the city of Zurich, no
children, no church tax, age 35, mirroring how the ESTV tax calculator
treats a gross salary. Rules in RULES are shown on the page with a source link.

TODO(you): paste the URL of the page your Zurich section 35 screenshot came from
and add it to RULES as "Zurich cantonal tax tariff" (assessment gate 3: every
rule must link to its source).
TODO(you): find official sources for the items marked "check source" below.
"""

from decimal import Decimal as D

TAX_YEAR = "2026"

ESTV_CIRCULAR_SOURCE = (
    "https://www.estv.admin.ch/dam/de/sd-web/vFK3ntWLQ4s4/2-215-D-2025-d.pdf"
)
SOCIAL_INSURANCE_SOURCE = "https://sozialversicherungen.admin.ch/de/d/6877/download"
ZH_RATES_SOURCE = (
    "https://www.zh.ch/de/steuern-finanzen/steuern/steuerstatistiken/"
    "aktuelle-gemeinde-steuerfuesse.html"
)
ESTV_CALCULATOR_SOURCE = "https://swisstaxcalculator.estv.admin.ch/"
UK_CH_SOCIAL_SECURITY_SOURCE = (
    "https://www.gov.uk/guidance/social-security-contributions-for-workers-"
    "coming-to-the-uk-from-the-eea-or-switzerland"
)

# --- Employee social security (hypothetical social security) -----------------
AHV_IV_EO_RATE = D("0.053")  # 4.35% + 0.7% + 0.25%
ALV_RATE = D("0.011")  # unemployment insurance
ALV_SALARY_CEILING = D("148200")  # no contribution above this (no solidarity rate)

# --- Deductions the ESTV calculator makes before tax -------------------------
# Accident insurance outside work, paid by the employee (calculator notes: 0.4%,
# salary capped at the maximum insured salary).
NBU_RATE = D("0.004")
NBU_SALARY_CEILING = D("148200")

# Pension fund (BVG). NOT part of hypothetical social security (brief), but the
# calculator deducts it when working out taxable income.
# check source: the 2026 BVG limits below should be confirmed on an official
# BSV / sozialversicherungen.admin.ch page. They reproduce the calculator's
# CHF 5,988 for a CHF 170,000 salary at age 35.
EMPLOYEE_AGE = 35
BVG_ENTRY_THRESHOLD = D("22680")
BVG_MIN_COORDINATED_SALARY = D("3780")
BVG_COORDINATION_DEDUCTION = D("26460")
BVG_UPPER_LIMIT = D("90720")  # salary above this is "extra-mandatory"
BVG_RATE_FROM_AGE = [  # (from age, total contribution rate on coordinated salary)
    (55, D("0.18")),
    (45, D("0.15")),
    (35, D("0.10")),
    (25, D("0.07")),
]
BVG_EXTRA_MANDATORY_RATE = D("0.07")
BVG_EMPLOYEE_SHARE = D("0.5")  # the calculator takes half as the employee's part

# check source: flat-rate professional expenses (3% of net salary, min 2,000,
# max 4,000) and the maximum insurance deduction. The calculator shows 4,000
# professional expenses and 2,900 (canton) / 1,800 (federal) insurance for the
# test case; the rates and limits are not spelled out in its notes.
PROFESSIONAL_EXPENSES_RATE = D("0.03")
PROFESSIONAL_EXPENSES_MIN = D("2000")
PROFESSIONAL_EXPENSES_MAX = D("4000")
INSURANCE_DEDUCTION_CANTON = D("2900")
INSURANCE_DEDUCTION_FEDERAL = D("1800")

# --- Direct federal tax, single person tariff 2026 (Art. 36 DBG) ---------------
# (taxable income from, tax at that income, extra tax per further CHF 100)
FEDERAL_TARIFF = [
    (D("15200"), D("0"), D("0.77")),
    (D("33200"), D("138.60"), D("0.88")),
    (D("43500"), D("229.20"), D("2.64")),
    (D("58000"), D("612.00"), D("2.97")),
    (D("76200"), D("1152.50"), D("5.94")),
    (D("82100"), D("1502.95"), D("6.60")),
    (D("108900"), D("3271.75"), D("8.80")),
    (D("141500"), D("6140.55"), D("11.00")),
    (D("185100"), D("10936.55"), D("13.20")),
    (D("793900"), D("91298.15"), D("0")),
]
FEDERAL_FLAT_FROM = D("794000")  # from here the tax is 11.5% of the whole income
FEDERAL_FLAT_RATE = D("0.115")
FEDERAL_MIN_TAX = D("25")  # amounts below this are not collected

# --- Canton of Zurich ---------------------------------------------------------
# Basic tax (einfache Staatssteuer), Grundtarif, section 35 para 1 StG, valid from
# tax period 2026. (width of the band in CHF, rate). None = all income above.
ZH_BASIC_TARIFF = [
    (D("7000"), D("0")),
    (D("5000"), D("0.02")),
    (D("4800"), D("0.03")),
    (D("8000"), D("0.04")),
    (D("9700"), D("0.05")),
    (D("11200"), D("0.06")),
    (D("13100"), D("0.07")),
    (D("17600"), D("0.08")),
    (D("34000"), D("0.09")),
    (D("33700"), D("0.10")),
    (D("53300"), D("0.11")),
    (D("69300"), D("0.12")),
    (None, D("0.13")),
]
ZH_CANTON_MULTIPLIER = D("0.95")  # Staatssteuerfuss 2026
ZH_CITY_MULTIPLIER = D("1.19")  # city of Zurich, without church tax
# check source: flat per-person tax shown by the ESTV calculator (CHF 24).
ZH_PERSONAL_TAX = D("24")

RULES = [
    {
        "name": "Swiss social security during the assignment",
        "detail": (
            "A worker posted to the UK for up to 2 years stays in the home "
            "country's system with a certificate of coverage (PDA1); the "
            "employer's liability follows the employee's. So Swiss AHV/IV/EO "
            "and unemployment insurance continue and no UK NI is due."
        ),
        "source": UK_CH_SOCIAL_SECURITY_SOURCE,
    },
    {
        "name": "Swiss employee contributions 2026",
        "detail": (
            "AHV/IV/EO 5.3%; unemployment insurance 1.1% on salary up to "
            "CHF 148,200."
        ),
        "source": SOCIAL_INSURANCE_SOURCE,
    },
    {
        "name": "Swiss direct federal tax tariff 2026 (single)",
        "detail": "Tariff for single taxpayers, valid from 1 January 2026.",
        "source": ESTV_CIRCULAR_SOURCE,
    },
    {
        "name": "Zurich tax multipliers 2026",
        "detail": (
            "Canton 95% and city of Zurich 119% (without church tax) of the "
            "basic cantonal tax."
        ),
        "source": ZH_RATES_SOURCE,
    },
    {
        "name": "Hypothetical tax method",
        "detail": (
            "Taxable income and deductions follow the ESTV tax calculator "
            "for a single employee aged 35 in the city of Zurich."
        ),
        "source": ESTV_CALCULATOR_SOURCE,
    },
]

ASSUMPTIONS = [
    "Swiss 2026 rules are used for every year of the assignment.",
    "Swiss social security (AHV/IV/EO and unemployment insurance) continues "
    "throughout, so no UK National Insurance is due. The 2-year limit is "
    "exactly met by the test case.",
    "Hypothetical Swiss tax follows the ESTV tax calculator for a single "
    "employee aged 35 in the city of Zurich, no children, no church tax.",
    "To reach taxable income the calculator also deducts estimated accident "
    "insurance (0.4%) and pension fund (BVG) contributions, flat-rate "
    "professional expenses and the maximum insurance deduction. BVG is not "
    "counted in hypothetical social security.",
    "No unemployment insurance solidarity contribution above CHF 148,200.",
]