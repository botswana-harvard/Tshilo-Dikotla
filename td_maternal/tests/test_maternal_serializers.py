import json

from django.core import serializers
from django.test.testcases import TestCase
from model_mommy import mommy

from edc_sync.models import OutgoingTransaction


from td.models import Appointment

from edc_call_manager.models import Call, Log
from edc_identifier.models import SubjectIdentifier
from edc_registration.models import RegisteredSubject

from .mixins import NegMotherMixin, AntenatalVisitsMotherMixin


class TestMaternalSerializers(AntenatalVisitsMotherMixin, NegMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalSerializers, self).setUp()
        self.appointment = Appointment.objects.get(
            visit_code='1000M',
            subject_identifier=self.subject_identifier)
        self.maternal_visit = self.get_maternal_visit('1000M')

    def test_antenatal_enrollment_deserialising(self):
        """ Creating specimenconsent should creates outgoingtransaction """
        call = Call.objects.get(subject_identifier=self.subject_identifier)
        log = Log.objects.get(call=call)
        registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
        print(self.subject_identifier, '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
#         subjectidentifier = SubjectIdentifier.objects.get(identifier=self.subject_identifier)
        outgoing_transactions = OutgoingTransaction.objects.all()
        self.assertGreater(outgoing_transactions.count(), 0)
        for outgoing_transaction in outgoing_transactions:
            json_tx = json.loads(outgoing_transaction.aes_decrypt(outgoing_transaction.tx))[0]
            for deserialised_obj in serializers.deserialize(
                    "json", outgoing_transaction.aes_decrypt(outgoing_transaction.tx),
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True):
                if json_tx.get('model') == 'td_maternal.maternalconsent':
                    self.assertEqual(self.maternal_consent.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternaleligibility':
                    self.assertEqual(self.maternal_eligibility.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.antenatalenrollment':
                    self.assertEqual(self.antenatal_enrollment.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternalvisit':
                    self.assertEqual(self.maternal_visit.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternalultrasoundinitial':
                    self.assertEqual(self.maternal_ultrasound.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td.appointment':
                    self.assertEqual(self.appointment.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'edc_call_manager.call':
                    self.assertEqual(call.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'edc_registration.registeredsubject':
                    self.assertEqual(registered_subject.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'edc_call_manager.log':
                    self.assertEqual(log.pk, deserialised_obj.object.pk)
#                 elif json_tx.get('model') == 'edc_identifier.subjectidentifier':
#                     self.assertEqual(subjectidentifier.pk, deserialised_obj.object.pk)

    def test_antenatal_enrollment_visit_crfs(self):
        """ Creating specimenconsent should creates outgoingtransaction """
        maternallocator = mommy.make_recipe(
            'td_maternal.maternallocator', maternal_visit=self.maternal_visit, appointment=self.appointment)
        maternalobstericalhistory = mommy.make_recipe('td_maternal.maternalobstericalhistory', maternal_visit=self.maternal_visit)
        maternalmedicalhistory = mommy.make_recipe('td_maternal.maternalmedicalhistory', maternal_visit=self.maternal_visit)
        maternaldemographics = mommy.make_recipe('td_maternal.maternaldemographics', maternal_visit=self.maternal_visit)
        maternalarvlifetimehistory = mommy.make_recipe('td_maternal.maternalarvlifetimehistory', maternal_visit=self.maternal_visit)
        maternalarvinthispreg = mommy.make_recipe('td_maternal.maternalarvinthispreg', maternal_visit=self.maternal_visit)
        maternalclinicalmeasurementsone = mommy.make_recipe('td_maternal.maternalclinicalmeasurementsone', maternal_visit=self.maternal_visit)
        outgoing_transactions = OutgoingTransaction.objects.all()
        self.assertGreater(outgoing_transactions.count(), 0)
        for outgoing_transaction in outgoing_transactions:
            json_tx = json.loads(outgoing_transaction.aes_decrypt(outgoing_transaction.tx))[0]
            for deserialised_obj in serializers.deserialize(
                    "json", outgoing_transaction.aes_decrypt(outgoing_transaction.tx),
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True):
                if json_tx.get('model') == 'td_maternal.maternallocator':
                    self.assertEqual(maternallocator.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternalobstericalhistory':
                    self.assertEqual(maternalobstericalhistory.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternalmedicalhistory':
                    self.assertEqual(maternalmedicalhistory.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternaldemographics':
                    self.assertEqual(maternaldemographics.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternalarvlifetimehistory':
                    self.assertEqual(maternalarvlifetimehistory.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternalarvpreg':
                    self.assertEqual(maternalarvinthispreg.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternalclinicalmeasurementsone':
                    self.assertEqual(maternalclinicalmeasurementsone.pk, deserialised_obj.object.pk)

    def test_antenatal_enrollmenttwo_crfs_deserialising(self):
        mommy.make('td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit, number_of_gestations=1)
        antenatalenrollmenttwo = mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo', subject_identifier=self.subject_identifier)
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='1010M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=appointment, reason='scheduled')

        maternallabdel = mommy.make_recipe(
            'td_maternal.maternallabdel', subject_identifier=self.subject_identifier)

        outgoing_transactions = OutgoingTransaction.objects.all()
        self.assertGreater(outgoing_transactions.count(), 0)
        for outgoing_transaction in outgoing_transactions:
            json_tx = json.loads(outgoing_transaction.aes_decrypt(outgoing_transaction.tx))[0]
            for deserialised_obj in serializers.deserialize(
                    "json", outgoing_transaction.aes_decrypt(outgoing_transaction.tx),
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True):
                if json_tx.get('model') == 'td_maternal.antenatalenrollmenttwo':
                    self.assertEqual(antenatalenrollmenttwo.pk, deserialised_obj.object.pk)
                elif json_tx.get('model') == 'td_maternal.maternalLabourdel':
                    self.assertEqual(maternallabdel.pk, deserialised_obj.object.pk)
