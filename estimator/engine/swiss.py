"""Hypothetical Swiss tax and social security (CHF).

Both are what the employee would have paid had they stayed in Zurich. The
employer deducts them from pay, which is why they reduce the employer's cost.

NOT BUILT YET. Until you implement them the page shows a "not built yet"
notice instead of a cost table. Put the rates and brackets you use in
estimator/data/ next to a source link, like uk_rates.py does.

TODO(you): hypothetical income tax
  Federal + Zurich cantonal + city of Zurich communal tax on salary + bonus,
  single, no children, no church tax. Sources: Swiss Federal Tax
  Administration (federal tax scale) and the Zurich cantonal tax office
  (cantonal base rates and the communal multipliers). You can sanity-check
  the total against the ESTV tax calculator, as the brief suggests.

TODO(you): hypothetical social security
  Employee AHV/IV/EO and unemployment insurance (ALV), no BVG. Check the
  rates and the ALV salary ceiling on the official AHV / ESTV pages.
"""

from decimal import Decimal as D


def hypothetical_income_tax_chf(gross_chf: D) -> D:
    raise NotImplementedError("Hypothetical Swiss income tax is not built yet.")


def hypothetical_social_security_chf(gross_chf: D) -> D:
    raise NotImplementedError("Hypothetical Swiss social security is not built yet.")
