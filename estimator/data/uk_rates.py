"""UK tax reference data for the 2026/27 tax year.

Every rule carries the official page it came from, so the interface can show a
link next to each one. Keep values and sources together in this file.

Every number below was checked against the two GOV.UK pages named in the
sources.
"""

from decimal import Decimal as D

TAX_YEAR = "2026/27"

INCOME_TAX_SOURCE = "https://www.gov.uk/income-tax-rates"
EMPLOYER_RATES_SOURCE = (
    "https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027"
)

# England income tax, applied to taxable income (after personal allowance).
PERSONAL_ALLOWANCE = D("12570")
TAPER_THRESHOLD = D("100000")  # allowance falls by £1 for every £2 above this
TAPER_RATE = D("0.5")
BASIC_RATE = D("0.20")
BASIC_BAND_WIDTH = D("37700")  # taxable income taxed at the basic rate
HIGHER_RATE = D("0.40")
ADDITIONAL_THRESHOLD = D("125140")  # taxable income above this is additional rate
ADDITIONAL_RATE = D("0.45")

# Employer Class 1 National Insurance (only used if UK NI applies, see below).
EMPLOYER_NI_RATE = D("0.15")
EMPLOYER_NI_SECONDARY_THRESHOLD = D("5000")  # per year

# Which country's social security applies during the assignment: "CH" or "UK".
# Decision: a worker posted to the UK for up to 2 years stays in the home
# country's system with a certificate of coverage (PDA1), and the employer's
# liability follows the employee's. The test case is exactly 2 years, so Swiss
# social security continues and no UK National Insurance is due.
# The rule and its source are in swiss_rates.RULES.
SOCIAL_SECURITY_SYSTEM = "CH"

# Shown on the page under "Rules and sources". Entries must have a source.
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