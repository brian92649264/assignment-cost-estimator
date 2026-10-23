from decimal import Decimal as D
from types import SimpleNamespace

from django.test import SimpleTestCase

from estimator.data import uk_benefits
from estimator.engine.calculator import (
    CASH,
    EXEMPT,
    REMOVAL,
    AssignmentInputs,
    Benefit,
    calculate,
)

FAKE_SWISS = SimpleNamespace(
    hypothetical_income_tax_chf=lambda gross: D("6000"),
    hypothetical_social_security_chf=lambda gross: D("4000"),
)


def make_inputs(benefits, years=2):
    return AssignmentInputs(
        salary_chf=D("100000"),
        bonus_chf=D("0"),
        years=years,
        chf_per_gbp=D("1"),
        benefits=benefits,
    )


class RemovalLimitTests(SimpleTestCase):
    def test_limit_is_eight_thousand(self):
        self.assertEqual(uk_benefits.REMOVAL_EXEMPTION_LIMIT, D("8000"))

    def test_costs_under_the_limit_are_not_taxed(self):
        result = calculate(
            make_inputs([Benefit("Moving", D("5000"), REMOVAL, True)]), swiss=FAKE_SWISS
        )
        self.assertEqual(result.years[0].gross_up.initial_pay, D("90000"))

    def test_only_the_excess_over_the_limit_is_taxed(self):
        benefits = [
            Benefit("Moving", D("6000"), REMOVAL, True),
            Benefit("Temporary housing", D("4000"), REMOVAL, True),
        ]
        result = calculate(make_inputs(benefits), swiss=FAKE_SWISS)
        year1 = result.years[0]
        self.assertEqual(year1.gross_up.initial_pay, D("92000"))
        lines = year1.sections[1].lines
        self.assertIn("Within the £8,000", lines[0].note)
        self.assertIn("£2,000 is above it and taxed", lines[1].note)

    def test_table_still_shows_the_full_cost_of_each_benefit(self):
        benefits = [
            Benefit("Moving", D("6000"), REMOVAL, True),
            Benefit("Temporary housing", D("4000"), REMOVAL, True),
        ]
        result = calculate(make_inputs(benefits), swiss=FAKE_SWISS)
        self.assertEqual(result.years[0].sections[1].total, D("10000"))

    def test_the_limit_is_shared_across_years(self):
        result = calculate(
            make_inputs([Benefit("Support", D("5000"), REMOVAL)]), swiss=FAKE_SWISS
        )
        self.assertEqual(result.years[0].gross_up.initial_pay, D("90000"))
        self.assertEqual(result.years[1].gross_up.initial_pay, D("92000"))

    def test_other_treatments_are_unaffected(self):
        benefits = [
            Benefit("Rent", D("36000"), CASH),
            Benefit("Exempt thing", D("1000"), EXEMPT, True),
        ]
        result = calculate(make_inputs(benefits, years=1), swiss=FAKE_SWISS)
        self.assertEqual(result.years[0].gross_up.initial_pay, D("126000"))


class BenefitRulesTests(SimpleTestCase):
    def test_every_benefit_rule_has_an_official_source(self):
        for rule in uk_benefits.RULES:
            self.assertTrue(rule["source"], rule["name"])
            self.assertIn("gov.uk", rule["source"], rule["name"])