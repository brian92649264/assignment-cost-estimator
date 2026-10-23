from decimal import Decimal as D

TAX_YEAR = "2026/27"

INCOME_TAX_SOURCE = "https://www.gov.uk/income-tax-rates"
EMPLOYER_RATES_SOURCE = (
    "https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027"
)

PERSONAL_ALLOWANCE = D("12570")
TAPER_THRESHOLD = D("100000")  
TAPER_RATE = D("0.5")
BASIC_RATE = D("0.20")
BASIC_BAND_WIDTH = D("37700")  
HIGHER_RATE = D("0.40")
ADDITIONAL_THRESHOLD = D("125140")  
ADDITIONAL_RATE = D("0.45")

EMPLOYER_NI_RATE = D("0.15")
EMPLOYER_NI_SECONDARY_THRESHOLD = D("5000")  

SOCIAL_SECURITY_SYSTEM = "CH"

RULES = [
    {
        "name": "UK income tax bands and personal allowance",
        "detail": (
            "20% basic, 40% higher and 45% additional rate; personal allowance "
            "withdrawn at £1 per £2 above £100,000."
        ),
        "source": INCOME_TAX_SOURCE,
    },
    {
        "name": "Employer National Insurance",
        "detail": "Employer rate and secondary threshold for 2026/27.",
        "source": EMPLOYER_RATES_SOURCE,
    },
]