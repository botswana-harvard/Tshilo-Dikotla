from model_mommy import mommy

from django.test import TestCase, tag

from ..models import MaternalEligibilityLoss


@tag('enrollment')
class TestMaternalEligibility(TestCase):
    """Test eligibility of a mother."""

    def test_eligibility_for_correct_age(self):
        """Test eligibility of a mother with the right age."""
        options = {'age_in_years': 26}
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility', **options)
        self.assertTrue(maternal_eligibility.is_eligible)

    def test_eligibility_for_under_age(self):
        """Test eligibility of a mother with under age."""
        options = {'age_in_years': 17}
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility', **options)
        self.assertFalse(maternal_eligibility.is_eligible)

    def test_eligibility_for_over_age(self):
        """Test eligibility of a mother with over age."""
        options = {'age_in_years': 51}
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility', **options)
        self.assertFalse(maternal_eligibility.is_eligible)

    def test_eligibility_who_has_omang(self):
        """Test eligibility of a mother with an Omang."""
        options = {'has_omang': 'Yes'}
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility', **options)
        self.assertTrue(maternal_eligibility.is_eligible)

    def test_eligibility_who_has_no_omang(self):
        """Test eligibility of a mother with no Omang."""
        options = {'has_omang': 'No'}
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility', **options)
        self.assertFalse(maternal_eligibility.is_eligible)

    def test_creates_lossform_on_fail(self):
        """Test loss record is created on fail."""
        options = {'has_omang': 'No'}
        self.assertEqual(MaternalEligibilityLoss.objects.all().count(), 0)
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility', **options)
        self.assertFalse(maternal_eligibility.is_eligible)
        self.assertEqual(MaternalEligibilityLoss.objects.all().count(), 1)
