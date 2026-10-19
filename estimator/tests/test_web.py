"""Form validation and page tests."""

from django.test import SimpleTestCase
from django.urls import reverse

from estimator.data import immigration, uk_rates
from estimator.forms import TEST_CASE_INITIAL, AssignmentForm


class FormValidationTests(SimpleTestCase):
    def test_test_case_is_accepted_as_given(self):
        form = AssignmentForm(TEST_CASE_INITIAL)
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_salary_gives_readable_message(self):
        data = {**TEST_CASE_INITIAL, "salary_chf": ""}
        form = AssignmentForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("Enter a value for base salary", form.errors["salary_chf"][0])

    def test_text_in_number_field_gives_readable_message(self):
        form = AssignmentForm({**TEST_CASE_INITIAL, "bonus_chf": "lots"})
        self.assertFalse(form.is_valid())
        self.assertIn("must be a number", form.errors["bonus_chf"][0])

    def test_negative_amount_rejected(self):
        form = AssignmentForm({**TEST_CASE_INITIAL, "moving_gbp": "-5"})
        self.assertFalse(form.is_valid())
        self.assertIn("cannot be negative", form.errors["moving_gbp"][0])

    def test_zero_exchange_rate_rejected(self):
        form = AssignmentForm({**TEST_CASE_INITIAL, "chf_per_gbp": "0"})
        self.assertFalse(form.is_valid())
        self.assertIn("greater than zero", form.errors["chf_per_gbp"][0])


class PageTests(SimpleTestCase):
    def test_page_loads_with_both_tabs(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, "Cost estimate")
        self.assertContains(response, "Immigration")

    def test_bad_post_shows_errors_not_a_crash(self):
        response = self.client.post(reverse("index"), {"salary_chf": "abc"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please fix the following")


class SourceTests(SimpleTestCase):
    """Every rule the page shows must carry an official link (assessment gate 3)."""

    def test_every_uk_rule_has_an_official_source(self):
        for rule in uk_rates.RULES:
            self.assertTrue(rule["source"], rule["name"])
            self.assertIn("gov.uk", rule["source"], rule["name"])

    def test_every_researched_immigration_topic_has_a_source(self):
        for topic in immigration.TOPICS:
            if topic["requirement"]:
                self.assertTrue(topic["source"], topic["title"])
