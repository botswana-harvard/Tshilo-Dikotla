import pprint

from dateutil.relativedelta import relativedelta
from model_mommy import mommy
from django.test import TestCase
from django.utils import timezone

from edc_constants.constants import POS, YES, NOT_APPLICABLE, NO
from edc_registration.models import RegisteredSubject

from td_maternal.enrollment_helper import EnrollmentHelper
from td_maternal.models import MaternalOffstudy

from .models import Appointment
from edc_sync.models import OutgoingTransaction
from django.core import serializers

pp = pprint.PrettyPrinter(indent=4)


class TestTd(TestCase):

    def test_registered_subject_created_by_consent(self):
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent')
        try:
            RegisteredSubject.objects.get(subject_identifier=maternal_consent.subject_identifier)
        except RegisteredSubject.DoesNotExist:
            self.fail('RegisteredSubject.DoesNotExist unexpectedly raised.')

    def test_appointment_maternal(self):
        """Assert no appointments for not eligible."""
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent')
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment_ineligible',
            subject_identifier=maternal_consent.subject_identifier)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertEqual(Appointment.objects.all().count(), 0)
        try:
            MaternalOffstudy.objects.get(subject_identifier=maternal_consent.subject_identifier)
        except MaternalOffstudy.DoesNotExist:
            self.fail('MaternalOffstudy.DoesNotExist unexpectedly raised.')

    def test_appointment_maternal2(self):
        """Assert has appointments for eligible."""
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent')
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment',
            subject_identifier=maternal_consent.subject_identifier,
            last_period_date=timezone.now() - relativedelta(days=280))
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(Appointment.objects.all().count(), 1)
        try:
            MaternalOffstudy.objects.get(subject_identifier=maternal_consent.subject_identifier)
            self.fail('MaternalOffstudy.DoesNotExist unexpectedly NOT raised.')
        except MaternalOffstudy.DoesNotExist:
            pass

    def test_ineligible(self):
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent')
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment_ineligible',
            subject_identifier=maternal_consent.subject_identifier)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def deserialised_obj(self, model_obj, outgoing_tx):
        for deserialised_obj in serializers.deserialize(
                "json", outgoing_tx.aes_decrypt(outgoing_tx.tx), use_natural_foreign_keys=True, use_natural_primary_keys=True):
            return deserialised_obj

    def test_antenatal_enrollment(self):
        """ Creating specimenconsent should creates outgoingtransaction """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent', maternal_eligibility=maternal_eligibility)
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', subject_identifier=maternal_consent.subject_identifier)
        outgoing_tx = OutgoingTransaction.objects.filter(tx_name='td_maternal.antenatalenrollment')
        self.assertTrue(outgoing_tx)
        deserialised_obj = self.deserialised_obj(antenatal_enrollment, outgoing_tx.first())
        self.assertEqual(antenatal_enrollment.pk, deserialised_obj.object.pk)

    def test_gestation_wks_lmp_below_16(self):
        """Test for a positive mother with evidence of hiv_status,
        will go on a valid regimen but weeks of gestation below 16."""
        options = {'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.now() - relativedelta(weeks=14)).date()}
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent')
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment',
            subject_identifier=maternal_consent.subject_identifier, **options)
        self.assertFalse(antenatal_enrollment.is_eligible)
        self.assertEqual(antenatal_enrollment.enrollment_hiv_status, POS)
        pp.pprint(EnrollmentHelper(antenatal_enrollment).as_dict())
        # self.off_study_visit_on_ineligible(antenatal_enrollment.subject_identifier)

    def test_on_therapy_for_atleast4weeks(self):
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent')
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment',
            subject_identifier=maternal_consent.subject_identifier)
        self.assertEqual(self.antenatal_enrollment.enrollment_hiv_status, POS)
        mommy.make_recipe(
            'td_maternal.maternallabourdel',
            subject_identifier=maternal_consent.subject_identifier,
            valid_regiment_duration=YES)
        enrollment_helper = EnrollmentHelper(antenatal_enrollment)
        self.assertTrue(enrollment_helper.eligible_after_delivery)
        self.assertTrue(enrollment_helper.is_eligible)
