"""Swiss tax and social security tests.

The main test reproduces the ESTV tax calculator's result for the test case
(CHF 170,000 gross, single, city of Zurich, 2026, no church tax).
"""

from decimal import Decimal as D

from django.test import SimpleTestCase

from estimator.data import swiss_rates
from estimator.engine import swiss


class EstvCalculatorTests(SimpleTestCase):
    """Figures read from the ESTV calculator result page."""

    def setUp(self):
        self.b = swiss.hypothetical_tax_breakdown(D("170000"))

    def test_deductions_match_calculator(self):
        self.assertEqual(round(self.b.ahv_iv_eo), 9010)
        self.assertEqual(round(self.b.alv), 1630)
        self.assertEqual(round(self.b.nbu), 593)
        self.assertEqual(round(self.b.bvg), 5988)
        self.assertEqual(round(self.b.net_income), 152779)

    def test_taxable_income_matches_calculator(self):
        self.assertEqual(round(self.b.taxable_income_canton), 145879)
        self.assertEqual(round(self.b.taxable_income_federal), 146979)

    def test_each_tax_matches_calculator(self):
        self.assertEqual(self.b.cantonal_tax, D("10130"))
        self.assertEqual(self.b.communal_tax, D("12689"))
        self.assertEqual(self.b.personal_tax, D("24"))
        self.assertEqual(self.b.federal_tax, D("6735"))

    def test_total_matches_calculator(self):
        self.assertEqual(self.b.total_tax, D("29578"))
        self.assertEqual(swiss.hypothetical_income_tax_chf(D("170000")), D("29578"))


class SocialSecurityTests(SimpleTestCase):
    def test_test_case_amount_and_no_bvg(self):
        # 5.3% of 170,000 + 1.1% of 148,200. BVG is deliberately not included.
        self.assertEqual(
            swiss.hypothetical_social_security_chf(D("170000")), D("10640.200")
        )

    def test_unemployment_insurance_stops_at_ceiling(self):
        self.assertEqual(swiss.alv(D("148200")), swiss.alv(D("500000")))
        self.assertEqual(swiss.alv(D("100000")), D("1100.000"))


class TariffTests(SimpleTestCase):
    def test_federal_tariff_at_published_points(self):
        self.assertEqual(swiss.federal_tax(D("108900")), D("3271.75"))
        self.assertEqual(swiss.federal_tax(D("141500")), D("6140.55"))

    def test_federal_tax_below_threshold_is_zero(self):
        self.assertEqual(swiss.federal_tax(D("15100")), D("0"))

    def test_federal_flat_rate_at_the_top(self):
        self.assertEqual(swiss.federal_tax(D("1000000")), D("115000.000"))

    def test_zurich_basic_tax_first_bands(self):
        self.assertEqual(swiss.zurich_basic_tax(D("7000")), D("0"))
        # 5,000 at 2% = 100
        self.assertEqual(swiss.zurich_basic_tax(D("12000")), D("100.00"))

    def test_zurich_bands_add_up_to_published_threshold(self):
        widths = [w for w, _ in swiss_rates.ZH_BASIC_TARIFF if w is not None]
        self.assertEqual(sum(widths), D("266700"))

    def test_taxable_income_rounds_down_to_100(self):
        self.assertEqual(
            swiss.zurich_basic_tax(D("145899.99")), swiss.zurich_basic_tax(D("145800"))
        )


class SwissSourceTests(SimpleTestCase):
    """Every Swiss rule shown on the page must link to an official site."""

    OFFICIAL = ("gov.uk", "admin.ch", "zh.ch")

    def test_every_swiss_rule_has_an_official_source(self):
        for rule in swiss_rates.RULES:
            self.assertTrue(rule["source"], rule["name"])
            self.assertTrue(
                any(domain in rule["source"] for domain in self.OFFICIAL), rule["name"]
            )


class PensionTests(SimpleTestCase):
    def test_no_pension_below_entry_threshold(self):
        self.assertEqual(swiss.bvg_employee(D("20000")), D("0"))

    def test_older_employee_pays_more(self):
        self.assertGreater(
            swiss.bvg_employee(D("100000"), age=50), swiss.bvg_employee(D("100000"), age=30)
        )