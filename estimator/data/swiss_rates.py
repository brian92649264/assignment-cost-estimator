from decimal import Decimal as D

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
BVG_LIMITS_SOURCE = "https://www.bsv.admin.ch/dam/de/sd-web/sAgdISSXenMT/d_Betr%C3%A4ge%202026.pdf"
FEDERAL_RETURN_GUIDE_SOURCE = "https://www.estv.admin.ch/dam/de/sd-web/oQ0wWcDmCJTS/2a-2026-de.pdf"
ZH_RETURN_GUIDE_SOURCE = (
    "https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/steuern-finanzen/"
    "steuern/natuerlichepersonen/2026/est-wegleitungen-uj/"
    "305%20Wegleitung%20ZH%202026%20UJ%20bf.pdf"
)
PERSONAL_TAX_SOURCE = "https://www.estv2.admin.ch/stp/sm/personalsteuer-de-fr.pdf"
ZH_TAX_LAW_SOURCE = (
    "https://www.zh.ch/de/politik-staat/gesetze-beschluesse/gesetzessammlung/"
    "zhlex-ls/erlass-631_1-1997_06_08-1999_01_01-132.html"
)

AHV_IV_EO_RATE = D("0.053")  
ALV_RATE = D("0.011")  
ALV_SALARY_CEILING = D("148200")  

NBU_RATE = D("0.004")
NBU_SALARY_CEILING = D("148200")

EMPLOYEE_AGE = 35
BVG_ENTRY_THRESHOLD = D("22680")
BVG_MIN_COORDINATED_SALARY = D("3780")
BVG_COORDINATION_DEDUCTION = D("26460")
BVG_UPPER_LIMIT = D("90720")  
BVG_RATE_FROM_AGE = [  
    (55, D("0.18")),
    (45, D("0.15")),
    (35, D("0.10")),
    (25, D("0.07")),
]
BVG_EXTRA_MANDATORY_RATE = D("0.07")
BVG_EMPLOYEE_SHARE = D("0.5")  

PROFESSIONAL_EXPENSES_RATE = D("0.03")
PROFESSIONAL_EXPENSES_MIN = D("2000")
PROFESSIONAL_EXPENSES_MAX = D("4000")
INSURANCE_DEDUCTION_CANTON = D("2900")
INSURANCE_DEDUCTION_FEDERAL = D("1800")

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
FEDERAL_FLAT_FROM = D("794000")  
FEDERAL_FLAT_RATE = D("0.115")
FEDERAL_MIN_TAX = D("25")  

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
ZH_CANTON_MULTIPLIER = D("0.95")  
ZH_CITY_MULTIPLIER = D("1.19")  

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
        "name": "Zurich cantonal tax tariff (single person)",
        "detail": (
            "Basic tariff of section 35(1) of the Zurich tax law, valid from tax "
            "period 2026: 0% on the first CHF 7,000, rising in bands to 13% on "
            "income above CHF 266,700."
        ),
        "source": ZH_TAX_LAW_SOURCE,
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
    {
        "name": "Swiss pension fund (BVG) limits 2026",
        "detail": (
            "Entry threshold CHF 22,680, coordination deduction CHF 26,460, "
            "upper limit CHF 90,720. Used only to work out taxable income."
        ),
        "source": BVG_LIMITS_SOURCE,
    },
    {
        "name": "Federal deductions (single person)",
        "detail": (
            "Flat-rate professional expenses of 3% of net salary (CHF 2,000 "
            "to 4,000) and an insurance deduction of CHF 1,800."
        ),
        "source": FEDERAL_RETURN_GUIDE_SOURCE,
    },
    {
        "name": "Zurich deductions",
        "detail": (
            "Flat-rate professional expenses of 3% of net salary (CHF 2,000 "
            "to 4,000) and an insurance deduction of CHF 2,900 for a single "
            "person."
        ),
        "source": ZH_RETURN_GUIDE_SOURCE,
    },
    {
        "name": "Zurich personal tax",
        "detail": "A flat personal tax of CHF 24 per person, charged by the municipality.",
        "source": PERSONAL_TAX_SOURCE,
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