import json
import pprint

from dateutil.relativedelta import relativedelta
from django.core import serializers
from django.test import TestCase
from django.test.utils import override_settings

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NOT_APPLICABLE
from edc_registration.models import RegisteredSubject
from edc_sync.models import OutgoingTransaction
from model_mommy import mommy

from td_maternal.enrollment_helper import EnrollmentHelper
from td_maternal.models import MaternalOffstudy

from ..models import Appointment

pp = pprint.PrettyPrinter(indent=4)


@override_settings(USE_L10N=False)
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
            last_period_date=(get_utcnow() - relativedelta(days=280)).date())
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(Appointment.objects.all().count(), 1)
        try:
            MaternalOffstudy.objects.get(subject_identifier=maternal_consent.subject_identifier)
            self.fail('MaternalOffstudy.DoesNotExist unexpectedly NOT raised.')
        except MaternalOffstudy.DoesNotExist:
            pass

    def test_antenatal_enrollment_deserialization(self):
        """ Creating specimenconsent should creates outgoingtransaction """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=maternal_eligibility)
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment', subject_identifier=maternal_consent.subject_identifier)
        outgoing_transactions = OutgoingTransaction.objects.all()
        self.assertGreater(outgoing_transactions.count(), 0)
        for outgoing_transaction in outgoing_transactions:
            json_tx = outgoing_transaction.aes_decrypt(outgoing_transaction.tx)
            for deserialised_obj in serializers.deserialize(
                    "json", outgoing_transaction.aes_decrypt(outgoing_transaction.tx),
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True):
                json_tx = json.loads(json_tx)
                pp.pprint(json_tx)
                try:
                    json_tx['td_maternal.maternalconsent']
                    self.assertEqual(maternal_consent.pk, deserialised_obj.object.pk)
                except KeyError:
                    pass
                if json_tx.get('model') == 'td_maternal.maternaleligibility':
                    self.assertEqual(maternal_eligibility.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.antenatalenrollment':
                    self.assertEqual(antenatal_enrollment.pk, deserialised_obj.object.pk)
                else:
                    pass
