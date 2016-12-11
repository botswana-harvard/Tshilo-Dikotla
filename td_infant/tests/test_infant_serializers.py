import json

from django.core import serializers
from django.test.testcases import TestCase

from model_mommy import mommy

from td.models import Appointment

from td_maternal.tests.test_mixins import NegMotherMixin, CompleteMaternalCrfsMixin
from .test_mixins import AddVisitInfantMixin
from edc_sync.models import OutgoingTransaction
from edc_visit_tracking.constants import SCHEDULED


class TestInfantSerializers(CompleteMaternalCrfsMixin, NegMotherMixin, AddVisitInfantMixin, TestCase):

    def setUp(self):
        super(TestInfantSerializers, self).setUp()
        self.appointment = Appointment.objects.get(
            visit_code='1000M',
            subject_identifier=self.subject_identifier)
        self.maternal_visit = self.get_maternal_visit('1000M')

    def test_infant_visit_2000_crfs(self):
        visit_2000_crfs = []
        maternal_lab_del = mommy.make_recipe(
            'td_maternal.maternallabdel', subject_identifier=self.subject_identifier)
        infant_birth = mommy.make_recipe(
            'td_infant.infantbirth',
            delivery_reference=maternal_lab_del.reference,
            subject_identifier=self.subject_identifier,
            birth_order=1)
        visit_2000_crfs.append(infant_birth)
        infant_visit = mommy.make_recipe(
            'td_infant.infantvisit', appointment=Appointment.objects.get(visit_code='2000'))
        visit_2000_crfs.append(infant_visit)
        infant_birth_data = mommy.make_recipe('td_infant.infantbirthdata', infant_visit=infant_visit)
        visit_2000_crfs.append(infant_birth_data)
        infant_birth_exam = mommy.make_recipe('td_infant.infantbirthexam', infant_visit=infant_visit)
        visit_2000_crfs.append(infant_birth_exam)
        infant_birthfeeding_vaccine = mommy.make_recipe(
            'td_infant.infantbirthfeedingvaccine', infant_visit=infant_visit)
        visit_2000_crfs.append(infant_birthfeeding_vaccine)
        infantbirtharv = mommy.make_recipe(
            'td_infant.infantbirtharv', infant_visit=infant_visit)
        visit_2000_crfs.append(infantbirtharv)
        infant_birth_data = mommy.make_recipe(
            'td_infant.infantcongenitalanomalies', infant_visit=infant_visit)
        visit_2000_crfs.append(infant_birth_data)
        for model_obj in visit_2000_crfs:
            cls = model_obj.__class__
            model_lower = '{}.{}'.format(cls._meta.app_label, cls._meta.model_name)
            outgoing_transaction = OutgoingTransaction.objects.get(tx_name=model_lower)
            for deserialised_obj in serializers.deserialize(
                    "json", outgoing_transaction.aes_decrypt(outgoing_transaction.tx),
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True):
                self.assertEqual(model_obj.pk, deserialised_obj.object.pk)
