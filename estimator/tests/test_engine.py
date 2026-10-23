from decimal import Decimal as D
from types import SimpleNamespace

from django.test import SimpleTestCase

from estimator.engine import uk_tax
from estimator.engine.calculator import (
    BIK,
    CASH,
    EXEMPT,
    AssignmentInputs,
    Benefit,
    calculate,
)
from estimator.engine.grossup import GrossUpError, gross_up

TOLERANCE = D("0.01")


class UkIncomeTaxTests(SimpleTestCase):
    def test_nothing_due_within_personal_allowance(self):
        self.assertEqual(uk_tax.income_tax(D("12570")), D("0"))

    def test_top_of_basic_band(self):
        self.assertEqual(uk_tax.income_tax(D("50270")), D("7540"))

    def test_allowance_intact_at_100k(self):
        self.assertEqual(uk_tax.income_tax(D("100000")), D("27432"))

    def test_allowance_fully_withdrawn_at_125140(self):
        self.assertEqual(uk_tax.personal_allowance(D("125140")), D("0"))
        self.assertEqual(uk_tax.income_tax(D("125140")), D("42516"))

    def test_taper_makes_marginal_rate_sixty_percent(self):
        extra = uk_tax.income_tax(D("110100")) - uk_tax.income_tax(D("110000"))
        self.assertEqual(extra, D("60"))


class GrossUpTests(SimpleTestCase):
    def test_flat_rate_has_closed_form(self):
        result = gross_up(D("1000"), lambda x: x * D("0.2"))
        self.assertLess(abs(result.tax - D("250")), TOLERANCE)

    def test_result_satisfies_the_equation(self):
        for pay in (D("20000"), D("60000"), D("95000"), D("140000"), D("300000")):
            result = gross_up(pay, uk_tax.income_tax)
            self.assertLess(abs(result.tax - uk_tax.income_tax(pay + result.tax)), TOLERANCE)

    def test_single_multiplication_would_be_wrong(self):
        pay = D("95000")
        result = gross_up(pay, uk_tax.income_tax)
        naive = uk_tax.income_tax(pay) / (1 - D("0.40"))
        self.assertGreater(abs(result.tax - naive), D("100"))

    def test_records_each_step(self):
        result = gross_up(D("60000"), uk_tax.income_tax)
        self.assertGreater(result.iterations, 1)
        self.assertEqual(result.steps[0].assumed_tax, D("0"))

    def test_raises_if_it_cannot_settle(self):
        with self.assertRaises(GrossUpError):
            gross_up(D("1000"), lambda x: x * D("2"), max_iterations=20)


class CalculatorTests(SimpleTestCase):
    fake_swiss = SimpleNamespace(
        hypothetical_income_tax_chf=lambda gross: gross * D("0.20"),
        hypothetical_social_security_chf=lambda gross: gross * D("0.06"),
    )

    def make_inputs(self, years=2):
        return AssignmentInputs(
            salary_chf=D("150000"),
            bonus_chf=D("20000"),
            years=years,
            chf_per_gbp=D("1.10"),
            benefits=[
                Benefit("Housing", D("36000"), BIK),
                Benefit("Relocation", D("4545.45"), CASH, year_one_only=True),
                Benefit("Moving", D("6000"), EXEMPT, year_one_only=True),
            ],
        )

    def test_one_off_benefits_only_in_year_one(self):
        result = calculate(self.make_inputs(), swiss=self.fake_swiss)
        year1, year2 = result.years
        self.assertEqual(len(year1.sections[1].lines), 3)
        self.assertEqual(len(year2.sections[1].lines), 1)

    def test_sections_in_required_order(self):
        result = calculate(self.make_inputs(), swiss=self.fake_swiss)
        titles = [s.title for s in result.years[0].sections]
        self.assertEqual(
            [t[:2] for t in titles], ["1.", "2.", "3.", "4."]
        )

    def test_employer_cost_is_pay_plus_benefits_plus_uk_tax_minus_deductions(self):
        result = calculate(self.make_inputs(), swiss=self.fake_swiss)
        year = result.years[0]
        home, benefits, host, deductions = year.sections
        self.assertEqual(
            year.employer_cost,
            home.total + benefits.total + host.total - deductions.total,
        )

    def test_totals_cover_every_year(self):
        result = calculate(self.make_inputs(years=2), swiss=self.fake_swiss)
        self.assertEqual(len(result.years), 2)
        self.assertEqual(result.total_cost, sum(y.employer_cost for y in result.years))
        self.assertGreater(result.multiple_of_home_pay, 1)
