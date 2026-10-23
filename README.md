# Assignment cost estimate: Switzerland to UK

A small Django tool that estimates what it costs an employer to send an employee
from Switzerland (city of Zurich) to the UK (London) on a tax-equalised
assignment, where the employer pays the UK tax. A second tab sets out the
immigration requirements.

**Loom walkthrough:** ADD YOUR LOOM LINK HERE

---

## Install and run

You need **Python 3.10 or newer**. No database, API keys or other services are
needed, and there is no `migrate` step.

**macOS / Linux**

```bash
git clone <this-repo-url>
cd assignment-cost-estimator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

**Windows (PowerShell)**

```powershell
git clone <this-repo-url>
cd assignment-cost-estimator
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python manage.py runserver
```

Then open <http://127.0.0.1:8000/>. The form opens pre-filled with the test case
from the brief. Press **Calculate cost** to see the cost table for both years.

## Run the tests

With the virtual environment set up as above:

```bash
python manage.py test
```

(On Windows: `.venv\Scripts\python manage.py test`.) There are 47 tests covering
UK tax, the gross-up, the Swiss tax (checked against the ESTV calculator), the
benefit rules, form validation and the pages.

---

## What the tool shows

**Cost estimate tab.** Inputs for home and host country, assignment length,
salary, bonus, exchange rate and each benefit with its UK tax treatment. For each
year the output table has four sections:

1. **Home pay**: salary and bonus, converted at the input exchange rate.
2. **Assignment benefits**: each tagged as taxable cash, taxable benefit in kind,
   not taxable, or a removal cost under the £8,000 exemption.
3. **Host tax and charges paid by the employer**: UK income tax including tax on
   tax, and employer National Insurance (nil here, see below).
4. **Deductions**: hypothetical Swiss income tax and social security, which
   reduce the employer's cost.

Below the table: the employer cost per year and for the whole assignment, as a
figure and as a multiple of home pay; the gross-up working step by step; the
assumptions; and every rule with a link to its official source.

**Immigration tab.** Work permit, business visit, passport, company duties, time
and cost, each with links to the GOV.UK pages it comes from.

### Test case result

| | Year 1 | Year 2 |
|---|---|---|
| Employer cost | £274,785 | £254,884 |
| Multiple of home pay | 1.78x | 1.65x |

Whole assignment: **£529,670, or 1.71x home pay**.

---

## How it works

```
config/                 Django settings and URLs (no database)
estimator/
  data/                 reference data: every rate sits next to its source link
    uk_rates.py         UK income tax and employer NI, 2026/27
    uk_benefits.py      UK tax treatment of benefits, £8,000 removal limit
    swiss_rates.py      Swiss social security, federal and Zurich tax, 2026
    immigration.py      immigration tab content and sources
  engine/               pure Python, no Django
    uk_tax.py           UK income tax with the personal allowance taper
    grossup.py          solves T = UKTax(I + T) by iteration
    swiss.py            hypothetical Swiss tax and social security
    calculator.py       builds the four-section table for each year
  forms.py              input validation with readable error messages
  views.py              one page, two tabs
  templates/, static/   HTML, CSS and a few lines of JavaScript for the tabs
  tests/                automated tests
```

**Calculation for each year**

1. Convert salary and bonus to pounds (home pay).
2. Work out the hypothetical Swiss tax and social security on salary plus bonus.
3. Work out the taxable benefits for the year.
4. Set **I** = home pay − hypothetical deductions + taxable benefits.
5. Gross up: find **T** such that **T = UKTax(I + T)**.
6. Employer cost = home pay + all benefits + T + employer NI − hypothetical deductions.

**The gross-up.** The UK tax the employer pays is itself taxable pay, so the tax
depends on itself. UK rates change between bands and the personal allowance is
withdrawn above £100,000, so no single multiplier works. `grossup.py` starts with
T = 0, computes UKTax(I + T), feeds the result back in, and repeats until the
answer changes by less than 1p. This always settles because the highest marginal
rate (60% in the allowance taper) is below 100%. The page shows every step.

---

## Key decisions

**Social security.** Under the UK rules for workers coming from Switzerland, a
worker posted to the UK for up to 2 years stays in the home country's system with
a certificate of coverage (PDA1), and the employer's liability follows the
employee's. The test case is exactly 2 years (6 April 2026 to 5 April 2028), so
Swiss social security continues and no UK National Insurance is due. The output
shows this as a nil employer NI line with the reason.
Source: [GOV.UK, social security for workers from the EEA or Switzerland](https://www.gov.uk/guidance/social-security-contributions-for-workers-coming-to-the-uk-from-the-eea-or-switzerland).

**Hypothetical Swiss tax.** Taxable income follows the Swiss Federal Tax
Administration's (ESTV) tax calculator for a single employee aged 35 in the city
of Zurich, no church tax. For CHF 170,000 gross the code gives **CHF 29,578**,
the same as the calculator (federal 6,735, cantonal 10,130, communal 12,689,
personal tax 24). The calculator also deducts estimated pension fund (BVG) and
accident insurance contributions when working out taxable income, so the code
does too. BVG is not counted in hypothetical social security, as the brief asks.

**Hypothetical Swiss social security.** AHV/IV/EO (5.3%) and unemployment
insurance (1.1% up to CHF 148,200): **CHF 10,640.20** a year.

**Benefits.**
- Housing paid straight to the landlord counts as earnings (HMRC: the employer
  is paying the employee's own rent), so it is taxed in full.
- The CHF 5,000 relocation allowance is treated as a fixed cash payment and taxed
  in full.
- Moving costs (£6,000) and temporary housing (£4,000) are qualifying removal
  costs. Only the first £8,000 of these is exempt, so £2,000 is taxed and grossed
  up.

## Assumptions

- UK 2026/27 rates for both years; England bands, as the employee works in London.
- Exchange rate fixed at £1 = CHF 1.10 for both years.
- The employee is UK tax resident in both years and leaves Swiss tax residence.
- The UK subsidiary runs the payroll and pays all UK income tax.
- No pension contributions or Gift Aid, so adjusted net income equals taxable pay.
- Swiss 2026 rules for both years.
- No UK National Insurance, including Class 1A on the £2,000 above the removal
  limit, while Swiss social security continues.
- Any separate relief for the cost of flights is ignored.

The full list is shown with the result.

## Sources

Every rule the tool uses is listed on the page with a link to its official
source. The main ones:

- [GOV.UK: Income Tax rates and allowances](https://www.gov.uk/income-tax-rates)
- [GOV.UK: Rates and thresholds for employers 2026 to 2027](https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027)
- [HMRC: Tax equalisation (HS212)](https://www.gov.uk/government/publications/tax-equalisation-hs212-self-assessment-helpsheet/tax-equalisation-2026-hs212)
- [HMRC: EIM11521, employer paying the employee's rent](https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim11521)
- [HMRC: EIM03103, the £8,000 removal costs exemption](https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03103)
- [ESTV: direct federal tax tariff 2026](https://www.estv.admin.ch/dam/de/sd-web/vFK3ntWLQ4s4/2-215-D-2025-d.pdf)
- [Zurich tax law (StG), section 35 tariff](https://www.zh.ch/de/politik-staat/gesetze-beschluesse/gesetzessammlung/zhlex-ls/erlass-631_1-1997_06_08-1999_01_01-132.html)
- [Zurich tax rates (Steuerfüsse) 2026](https://www.zh.ch/de/steuern-finanzen/steuern/steuerstatistiken/aktuelle-gemeinde-steuerfuesse.html)
- [Swiss social insurance contributions 2026](https://sozialversicherungen.admin.ch/de/d/6877/download)
- [GOV.UK: Senior or Specialist Worker visa](https://www.gov.uk/senior-specialist-worker-visa)

Fees and rates were checked on 20 to 23 October 2026.

## Limitations

- One route only: Switzerland (city of Zurich) to the UK (London).
- Single employee with no children; the Swiss calculation assumes age 35.
- No pension, Class 1A or separate travel relief beyond what is listed above.

---

## AI tools used

<!-- Edit this to describe accurately what YOU used and what you did yourself. -->

I used **Claude (Anthropic)** throughout this project:

- **Code:** scaffolding the Django project, buiding project codebase, and tests.
- **Research:** finding and reading the official GOV.UK, HMRC, ESTV and canton of
  Zurich pages, and summarising the rules.

I chose the stack and the approach, made the decisions on social security, the
Swiss tax method and the benefit treatment, checked the figures against the
official pages myself (including running the ESTV tax calculator), and changed
the design of the pages. 