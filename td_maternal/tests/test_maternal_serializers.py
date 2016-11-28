from django.core import serializers
from django.test.testcases import TestCase
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_registration.models import RegisteredSubject
from edc_sync.models import OutgoingTransaction


from model_mommy import mommy

from td.models import Appointment


class TestMaternalSerializers(TestCase):

    def test_enrollments_deserialization(self):
        """ Creating specimenconsent should creates outgoingtransaction """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent', maternal_eligibility=maternal_eligibility)
        antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', subject_identifier=maternal_consent.subject_identifier)
        antenatal_enrollment_two = mommy.make_recipe('td_maternal.antenatalenrollment', subject_identifier=maternal_consent.subject_identifier)
        maternallabourdel = mommy.make('td_maternal.maternallabourdel', registered_subject=maternal_consent.registered_subject)
        specimen_consent = mommy.make('td_maternal.specimenconsent', registered_subject=maternal_consent.registered_subject)
        outgoing_transactions = OutgoingTransaction.objects.all()
        self.assertGreater(outgoing_transactions.count(), 0)
        for outgoing_transaction in outgoing_transactions:
            json_tx = outgoing_transaction.aes_decrypt(outgoing_transaction.tx)
            for deserialised_obj in serializers.deserialize(
                    "json", outgoing_transaction.aes_decrypt(outgoing_transaction.tx),
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True):
                if json_tx.get('model') == 'td_maternal.maternalconsent':
                    self.assertEqual(maternal_consent.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternaleligibility':
                    self.assertEqual(maternal_eligibility.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.antenatalenrollment':
                    self.assertEqual(antenatal_enrollment.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.antenatalenrollmenttwo':
                    self.assertEqual(antenatal_enrollment_two.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternallabourdel':
                    self.assertEqual(maternallabourdel.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.specimenconsent':
                    self.assertEqual(specimen_consent.pk, deserialised_obj.object.pk)
                else:
                    print(json_tx.get('model'))

    def test_antenatal_enrollment_visit_crfs(self):
        """ Creating specimenconsent should creates outgoingtransaction """
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent = mommy.make_recipe('td_maternal.maternalconsent', maternal_eligibility=maternal_eligibility)
        mommy.make_recipe('td_maternal.antenatalenrollment', subject_identifier=maternal_consent.subject_identifier)
        mommy.make_recipe('td_maternal.antenatalenrollment', subject_identifier=maternal_consent.subject_identifier)
        mommy.make('td_maternal.maternallabourdel', registered_subject=maternal_consent.registered_subject)
        mommy.make('td_maternal.specimenconsent', registered_subject=maternal_consent.registered_subject)
        appointment = Appointment.objects.get(
            visit_code='1000', subject_identifier=maternal_consent.registered_subject.subject_identifier)
        maternalvisit = mommy.make_recipe('td_maternal.maternalvisit', appointment=appointment)
        outgoing_transactions = OutgoingTransaction.objects.all()
        self.assertGreater(outgoing_transactions.count(), 0)
        for outgoing_transaction in outgoing_transactions:
            json_tx = outgoing_transaction.aes_decrypt(outgoing_transaction.tx)
            for deserialised_obj in serializers.deserialize(
                    "json", outgoing_transaction.aes_decrypt(outgoing_transaction.tx),
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True):
                if json_tx.get('model') == 'td_maternal.maternalvisit':
                    self.assertEqual(maternalvisit.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td.appointment':
                    self.assertEqual(appointment.pk, deserialised_obj.object.pk)
