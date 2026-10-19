# Assignment cost estimate: Switzerland to UK

A small Django tool that estimates what it costs an employer to send an employee from Switzerland to the UK for two years (tax equalisation, employer pays UK tax), and what immigration steps are needed. An exercise, not tax advice.

Loom walkthrough: TODO add link

## Install and run

Needs Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000/. The form opens pre-filled with the test case; press **Calculate cost**.

There is no database and no `migrate` step.

## Run the tests

```bash
python manage.py test
```

## How it works

- `estimator/engine/uk_tax.py`: UK income tax bands, personal allowance taper, employer NI.
- `estimator/engine/grossup.py`: solves `T = UKTax(I + T)` by iteration (tax on tax).
- `estimator/engine/swiss.py`: hypothetical Swiss income tax and social security.
- `estimator/engine/calculator.py`: builds the four-section cost table for each year.
- `estimator/data/`: tax rates and immigration rules, each with its official source link.
- `estimator/forms.py`: input validation with readable error messages.

## Social security decision

TODO: state which country's system applies during the assignment, the rule you applied, and the source.

## AI tools used

TODO: edit to match what you actually used. Claude (Anthropic) was used to scaffold the project structure, the Django boilerplate and the first draft of the engine, form and test files. The tax and immigration rules, sources and figures were researched and verified by hand.

## Status

- [ ] Verify every UK figure in `estimator/data/uk_rates.py` against its source, then set `VERIFIED = True`
- [ ] Build hypothetical Swiss income tax and social security (`engine/swiss.py`)
- [ ] Decide the social security system and cite the source
- [ ] Research the immigration tab (`data/immigration.py`)
- [ ] Add the Loom link and finish the sections above
