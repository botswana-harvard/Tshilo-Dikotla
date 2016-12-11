from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from django.apps import apps as django_apps
from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NO, NOT_APPLICABLE
from edc_identifier.models import IdentifierModel

from td.constants import INFANT
from td_list.models import DeliveryComplications

from ..enrollment_helper import EnrollmentHelper
from ..forms import MaternalLabDelForm

from .test_mixins import PosMotherMixin


class TestMaternalLabDel(PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalLabDel, self).setUp()
        self.add_maternal_visit('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        complications = DeliveryComplications.objects.create(
            hostname_created="django", name="None",
            short_name="None", created=get_utcnow(),
            user_modified="", modified=get_utcnow(),
            hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None,
            revision=":develop:")
        self.options = {
            'report_datetime': get_utcnow(),
            'delivery_datetime': get_utcnow(),
            'subject_identifier': self.subject_identifier,
            'delivery_time_estimated': NO,
            'labour_hrs': '3',
            'delivery_complications': [complications.id],
            'delivery_hospital': 'Lesirane',
            'mode_delivery': 'spontaneous vaginal',
            'csection_reason': NOT_APPLICABLE,
            'live_infants_to_register': 1,
            'valid_regimen_duration': YES,
            'arv_initiation_date': (get_utcnow() - relativedelta(weeks=6)).date()
        }

    def test_new_infant_identifiers(self):
        self.make_delivery()
        self.assertEqual(IdentifierModel.objects.filter(linked_identifier=self.subject_identifier).count(), 1)
        self.assertTrue(
            IdentifierModel.objects.get(linked_identifier=self.subject_identifier).identifier.endswith('10'))

    def test_new_infant_registration(self):
        RegisteredSubject = django_apps.get_app_config('edc_registration').model
        self.make_delivery()
        self.assertEqual(RegisteredSubject.objects.filter(
            subject_type=INFANT,
            registration_status='DELIVERED',
            relative_identifier=self.maternal_consent.subject_identifier).count(), 1)

    def test_on_therapy_for_atleast4weeks(self):
        self.assertEqual(self.antenatal_enrollment.enrollment_hiv_status, POS)
        self.make_delivery(valid_regimen_duration=YES)
        enrollment_helper = EnrollmentHelper(self.antenatal_enrollment)
        self.assertTrue(enrollment_helper.is_eligible)

    def test_not_therapy_for_atleast4weeks(self):
        self.assertEqual(self.antenatal_enrollment.enrollment_hiv_status, POS)
        self.make_delivery(valid_regimen_duration=YES)
        enrollment_helper = EnrollmentHelper(self.antenatal_enrollment)
        self.assertFalse(enrollment_helper.is_eligible)

    def test_valid_regimen_duration_hiv_pos_only_na(self):
        self.options.update(valid_regimen_duration=NOT_APPLICABLE)
        form = MaternalLabDelForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant is HIV+ and should have a valid regimen duration. Please correct.', errors)

    def test_valid_regimen_duration_hiv_pos_only_no_init_date(self):
        self.options.update(arv_initiation_date=None)
        form = MaternalLabDelForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated participant was on a valid regimen, '
                      'please give a valid ARV initiation date.', errors)

    def test_valid_regimen_duration_hiv_pos_only_invalid_init_date(self):
        self.options.update(arv_initiation_date=(get_utcnow() - relativedelta(weeks=1)).date())
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        form = MaternalLabDelForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that the mother was on her ARV regimen for a valid duration '
            'yet her delivery date is within 4weeks of her ART initiation date. Please correct.', errors)
