from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, tag

from model_mommy import mommy

from ..models import MaternalConsent


@tag('consent', 'enrollment')
class TestConsent(TestCase):

    def test_cannot_create_consent_without_eligibility(self):
        """Assert adding a consent without MaternalEligibility first raises an Exception."""
        try:
            mommy.make_recipe('td_maternal.maternalconsent')
            self.fail('Exception not raised')
        except (IntegrityError, ValidationError):
            pass

    def test_consent_allocates_subject_identifier(self):
        """Assert consent creates a subject identifier."""
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        mommy.make_recipe(
            'td_maternal.maternalconsent',
            maternal_eligibility_reference=maternal_eligibility.reference)
        RegisteredSubject = django_apps.get_app_config('edc_registration').model
        rs = RegisteredSubject.objects.all()[0]
        try:
            MaternalConsent.objects.get(subject_identifier=rs.subject_identifier)
        except MaternalConsent.DoesNotExist:
            self.fail('MaternalConsent.DoesNotExist unexpectedly raised')

    def test_consent_finds_maternal_eligibility(self):
        """Assert consent updates reference from MaternalEligibility."""
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        mommy.make_recipe(
            'td_maternal.maternalconsent',
            maternal_eligibility_reference=maternal_eligibility.reference)
        try:
            MaternalConsent.objects.get(maternal_eligibility_reference=maternal_eligibility.reference)
        except MaternalConsent.DoesNotExist:
            self.fail('MaternalConsent.DoesNotExist unexpectedly raised')
