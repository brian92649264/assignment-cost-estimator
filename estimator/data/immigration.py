"""Immigration requirements shown on the Immigration tab.

Each topic needs a `requirement` (plain-English statement) and a `source`
(link to the official page). Topics with requirement=None render as
"Not researched yet", so the page never shows an uncited claim.

TODO(you): research each topic and fill it in. Starting points to check:
- Work permit: the Global Business Mobility "Senior or Specialist Worker"
  route is the likely candidate for an overseas company sending staff to its
  UK subsidiary. Confirm the employment-length rule against the test case
  (3 years with the employer), the salary threshold, and the fee.
- Business visit: GOV.UK "Visit the UK" and the Electronic Travel Authorisation
  (ETA) pages. Check what applies to Swiss nationals and what activities a
  business visitor may do.
- Passport: GOV.UK passport validity rules for entering the UK.
- Company obligations: sponsor licence, certificate of sponsorship, and so on.
- Time and cost: processing times and fees from the official fees page.
"""

TOPICS = [
    {
        "key": "work_permit",
        "title": "Work permit",
        "requirement": None,
        "source": None,
    },
    {
        "key": "business_visit",
        "title": "Business visit before the assignment",
        "requirement": None,
        "source": None,
    },
    {
        "key": "passport",
        "title": "Passport requirements",
        "requirement": None,
        "source": None,
    },
    {
        "key": "company_obligations",
        "title": "What the company must do",
        "requirement": None,
        "source": None,
    },
    {
        "key": "time_and_cost",
        "title": "How long it takes and what it costs",
        "requirement": None,
        "source": None,
    },
]
