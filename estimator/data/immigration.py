"""Immigration requirements shown on the Immigration tab.

Each topic is one box: a title, a short summary (2 to 3 sentences) and the
official GOV.UK pages the summary came from.

Researched on 20 October 2026 from GOV.UK. Fees and thresholds change often:
re-check each figure against its page before submitting. Home Office fees are
from the table effective 8 October 2026.

Test case: a Swiss national paid CHF 150,000 salary (about GBP 136,000 at
CHF 1.10), sent by their Swiss employer to its UK subsidiary for 2 years after
3 years with the company.
"""

VISA_OVERVIEW = "https://www.gov.uk/senior-specialist-worker-visa"
VISA_ELIGIBILITY = "https://www.gov.uk/senior-specialist-worker-visa/eligibility"
VISA_COSTS = "https://www.gov.uk/senior-specialist-worker-visa/how-much-it-costs"
VISA_DOCUMENTS = "https://www.gov.uk/senior-specialist-worker-visa/documents-you-need-to-apply"
SPONSORSHIP_OVERVIEW = "https://www.gov.uk/uk-visa-sponsorship-employers"
SKILLS_CHARGE = "https://www.gov.uk/uk-visa-sponsorship-employers/immigration-skills-charge"
GBM_SPONSOR_GUIDANCE = (
    "https://www.gov.uk/government/publications/sponsor-a-global-business-mobility-worker/"
    "workers-and-temporary-workers-sponsor-a-global-business-mobility-worker-accessible"
)
FEES_TABLE = (
    "https://www.gov.uk/government/publications/visa-regulations-revised-table/"
    "home-office-immigration-and-nationality-fees-8-october-2026"
)
VISITING_AS_SWISS = "https://www.gov.uk/guidance/visiting-the-uk-after-brexit"
BUSINESS_VISIT = "https://www.gov.uk/standard-visitor/visit-on-business"
ETA = "https://www.gov.uk/guidance/electronic-travel-authorisation-eta"
SOCIAL_SECURITY = (
    "https://www.gov.uk/guidance/social-security-contributions-for-workers-"
    "coming-to-the-uk-from-the-eea-or-switzerland"
)

TOPICS = [
    {
        "key": "work_permit",
        "title": "Work permit (visa)",
        "summary": (
            "The employee needs a Senior or Specialist Worker visa, sponsored by "
            "the UK company, with a certificate of sponsorship and pay of at least "
            "£52,500 a year (or the going rate for the job). The test case meets "
            "the service rule, and a 2-year assignment fits within the visa length."
        ),
        "sources": [
            {"label": "Visa eligibility", "url": VISA_ELIGIBILITY},
            {"label": "Visa overview", "url": VISA_OVERVIEW},
            {"label": "Sponsorship for employers", "url": SPONSORSHIP_OVERVIEW},
        ],
    },
    {
        "key": "business_visit",
        "title": "Business visit",
        "summary": (
            "No visa is needed for a short business trip, but Swiss citizens need "
            "an electronic travel authorisation (ETA), which costs £20. Meetings, "
            "contracts and site visits are allowed for up to 6 months, but paid or "
            "unpaid work for a UK company is not."
        ),
        "sources": [
            {"label": "Visiting the UK as a Swiss citizen", "url": VISITING_AS_SWISS},
            {"label": "Business visits", "url": BUSINESS_VISIT},
            {"label": "ETA", "url": ETA},
        ],
    },
    {
        "key": "passport",
        "title": "Passport",
        "summary": (
            "The work visa needs a valid passport, or another document showing "
            "identity and nationality. For a business visit the passport must be "
            "valid for the whole stay. Tuberculosis test results are only needed "
            "for people from listed countries."
        ),
        "sources": [
            {"label": "Visa documents", "url": VISA_DOCUMENTS},
            {"label": "Visiting the UK as a Swiss citizen", "url": VISITING_AS_SWISS},
        ],
    },
    {
        "key": "company_obligations",
        "title": "Company duties",
        "summary": (
            "The UK company needs a sponsor licence and must be linked to the Swiss "
            "company by common ownership or control. It must assign a certificate "
            "of sponsorship, pay the sponsorship and skills charges, and keep "
            "records for the worker. A PDA1 certificate keeps the employee in Swiss "
            "social security."
        ),
        "sources": [
            {"label": "Sponsor guidance", "url": GBM_SPONSOR_GUIDANCE},
            {"label": "Visa eligibility", "url": VISA_ELIGIBILITY},
            {"label": "Social security", "url": SOCIAL_SECURITY},
        ],
    },
    {
        "key": "time",
        "title": "Time to get",
        "summary": (
            "A visa decision usually takes about 3 weeks when applying from outside "
            "the UK. A faster decision is available for a fee of £500 (priority) or "
            "£1,000 (super priority). The visa application must be made within "
            "3 months of getting the certificate of sponsorship."
        ),
        "sources": [
            {"label": "Visa overview", "url": VISA_OVERVIEW},
            {"label": "Fee table", "url": FEES_TABLE},
            {"label": "Visa eligibility", "url": VISA_ELIGIBILITY},
        ],
    },
    {
        "key": "cost",
        "title": "Cost",
        "summary": (
            "The employee pays an £819 visa fee and usually £1,035 a year for the "
            "health surcharge, and must show £1,270 in savings unless the employer "
            "covers the first month. The employer pays £525 for the certificate and "
            "a £2,640 skills charge for 2 years, plus £1,682 for a sponsor licence "
            "if it has none."
        ),
        "sources": [
            {"label": "Visa costs", "url": VISA_COSTS},
            {"label": "Fee table", "url": FEES_TABLE},
            {"label": "Skills charge", "url": SKILLS_CHARGE},
        ],
    },
]