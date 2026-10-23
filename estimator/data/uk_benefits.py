from decimal import Decimal as D

REMOVAL_EXEMPTION_LIMIT = D("8000")

EIM_RENT = "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim11521"
EIM_REMOVAL_EXEMPTION = "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03103"
EIM_REMOVAL_CONDITIONS = "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03104"
EIM_TEMPORARY_ACCOMMODATION = "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03117"
RELOCATION_WHAT_TO_REPORT = "https://www.gov.uk/expenses-and-benefits-relocation/what-to-report-and-pay"
HS212 = (
    "https://www.gov.uk/government/publications/tax-equalisation-hs212-"
    "self-assessment-helpsheet/tax-equalisation-2026-hs212"
)

HOUSING_NOTE = "Rent paid to the landlord for the employee counts as earnings."
RELOCATION_NOTE = "Assumed a fixed cash allowance, not paid against receipts, so taxed in full."
MOVING_NOTE = "Assumed to be qualifying removal costs (flights and shipping)."
TEMP_HOUSING_NOTE = "Qualifies when the employee then moves into permanent accommodation."

RULES = [
    {
        "name": "Tax paid by the employer is taxable pay",
        "detail": (
            "Under tax equalisation, tax the employer pays for the employee is "
            "itself taxable pay, so it is grossed up."
        ),
        "source": HS212,
    },
    {
        "name": "Employer-paid rent",
        "detail": (
            "When an employer pays an employee's own rent or bills, including "
            "directly to the landlord, it counts as earnings and is taxed."
        ),
        "source": EIM_RENT,
    },
    {
        "name": "Removal costs: first £8,000 not taxed",
        "detail": (
            "The first £8,000 of qualifying removal expenses and benefits paid "
            "by the employer is exempt. Only the amount above £8,000 is taxed."
        ),
        "source": EIM_REMOVAL_EXEMPTION,
    },
    {
        "name": "Removal costs: only the excess is charged",
        "detail": "Employers report and pay tax only on the amount above £8,000.",
        "source": RELOCATION_WHAT_TO_REPORT,
    },
    {
        "name": "Removal costs: conditions",
        "detail": (
            "The move must change the employee's main residence because of a "
            "new job, and costs must be incurred by the end of the tax year "
            "after the one in which the job starts. Someone who becomes UK "
            "tax resident is usually accepted as having changed residence."
        ),
        "source": EIM_REMOVAL_CONDITIONS,
    },
    {
        "name": "Temporary accommodation",
        "detail": (
            "Temporary accommodation is covered when the employee intends to "
            "move into permanent accommodation to complete the relocation."
        ),
        "source": EIM_TEMPORARY_ACCOMMODATION,
    },
]

ASSUMPTIONS = [
    "Rent paid directly to the landlord is treated as taxable earnings, and "
    "is taxed in full each year.",
    "The relocation allowance is a fixed cash payment, not reimbursed against "
    "receipts, so it is taxed in full.",
    "Moving costs and temporary housing are qualifying removal costs. Together "
    "they share one £8,000 exemption for the whole assignment; the excess is "
    "taxed and the tax is grossed up.",
    "Any separate relief for the cost of flights is ignored.",
    "No UK National Insurance, including Class 1A on the taxable excess, is "
    "assumed to be due while Swiss social security continues.",
]