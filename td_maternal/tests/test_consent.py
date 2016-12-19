from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, tag
from dateutil.relativedelta import relativedelta

from django.utils import timezone

from model_mommy import mommy

from edc_base.utils import get_utcnow

from ..models import MaternalConsent
from td_maternal.forms import MaternalConsentForm

from .test_mixins import MaternalReferenceDateMixin


@tag('consent', 'enrollment')
class TestConsent(MaternalReferenceDateMixin, TestCase):

    def test_cannot_create_consent_without_eligibility(self):
        """Assert adding a consent without MaternalEligibility first raises an Exception."""
        try:
            mommy.make_recipe(
                'td_maternal.maternalconsent',
                consent_datetime=self.get_utcnow(),
            )
            self.fail('Exception not raised')
        except (IntegrityError, ValidationError):
            pass

    def test_consent_allocates_subject_identifier(self):
        """Assert consent creates a subject identifier."""
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        mommy.make_recipe(
            'td_maternal.maternalconsent',
            consent_datetime=self.get_utcnow(),
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
            consent_datetime=self.get_utcnow(),
            maternal_eligibility_reference=maternal_eligibility.reference)
        try:
            MaternalConsent.objects.get(maternal_eligibility_reference=maternal_eligibility.reference)
        except MaternalConsent.DoesNotExist:
            self.fail('MaternalConsent.DoesNotExist unexpectedly raised')


class TestConsentForm(TestCase):
    """Test consent form validations not at the base."""

    def test_dob_n_age_dnt_match(self):
        """Assert if the dob on the consent and age in year on eligibility do not match."""
        maternal_eligibility = mommy.make_recipe(
            'td_maternal.maternaleligibility',
            age_in_years=55,
            report_datetime=get_utcnow() - relativedelta(years=2))
        data = {
            'maternal_eligibility_reference': maternal_eligibility.reference,
            'subject_identifier': None,
            'study_site': '40',
            'consent_datetime': get_utcnow() - relativedelta(years=2),
            'dob': timezone.datetime(1989, 7, 7).date(),
            'first_name': 'ZEST',
            'last_name': 'ZEST',
            'initials': 'ZZ',
            'gender': 'F',
            'identity': '222222222',
            'confirm_identity': '222222222',
            'identity_type': 'OMANG',
            'is_dob_estimated': '-'}

        form = MaternalConsentForm(data=data)
        self.assertFalse(form.is_valid())
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'The date of birth entered does not match the age on the.', errors)
