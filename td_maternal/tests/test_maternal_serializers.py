from django.utils import timezone
from django.core import serializers
from django.test.testcases import TestCase

from edc_constants.constants import YES
from edc_sync.models import OutgoingTransaction

from model_mommy import mommy

from td.models import RegisteredSubject
from td_maternal.models import SpecimenConsent

from ..models import MaternalEligibility
from .factories import MaternalEligibilityFactory, MaternalConsentFactory
from ..models import MaternalConsent


class TestMaternalSerializers(TestCase):

    def test_maternaleligibility_serializer(self):
        """ Creating maternaleligibility should creates outgoingtransaction """
        mommy.make(MaternalEligibility)
        print (MaternalEligibility.objects.all())
        print(OutgoingTransaction.objects.all())
        self.assertEqual(OutgoingTransaction.objects.filter(tx_name='td_maternal.maternaleligibility').count(), 1)

    def test_maternaleligibility_deserialize(self):
        """ Serialized maternaleligibility record should be able deserialized. """
        maternal_eligibility = mommy.make(MaternalEligibility)
        outgoing_transaction = OutgoingTransaction.objects.last()
        deserialized_obj = serializers.deserialize(
            "json", self.aes_decrypt(outgoing_transaction.tx),
            use_natural_foreign_keys=True, use_natural_primary_keys=True)
        self.assertEqual(maternal_eligibility.pk, deserialized_obj.pk)

    def test_maternalconsent_serialize(self):
        """ Creating maternalconsent should creates outgoingtransaction """
        maternal_eligibility = mommy.make(MaternalEligibility)
        mommy.make(
            MaternalConsent,
            maternal_eligibility=maternal_eligibility,
            identity="111121111",
            confirm_identity="111121111",
            study_site='40',
            is_literate=YES
        )
        self.assertEqual(OutgoingTransaction.objects.filter(tx_name='td_maternal.maternalconsent').count(), 1)

    def test_maternalconsent_deserialize(self):
        """ Serialized maternalconsent record should be able deserialized. """
        maternal_eligibility = mommy.make(MaternalEligibility)
        maternal_consent = mommy.make(MaternalConsent, maternal_eligibility=maternal_eligibility)
        outgoing_tx = OutgoingTransaction.objects.get(tx_name='td_maternal.maternalconsent')
        deserialized_obj = serializers.deserialize(
            "json", self.aes_decrypt(outgoing_tx.tx),
            use_natural_foreign_keys=True, use_natural_primary_keys=True)
        self.assertEqual(maternal_consent.pk, deserialized_obj.pk)

    def test_specimen_consent_serialize(self):
        """ Creating specimenconsent should creates outgoingtransaction """
        maternal_eligibility = mommy.make(MaternalEligibility)
        maternal_consent = mommy.make(MaternalConsent, maternal_eligibility=maternal_eligibility)
        registered_subject = RegisteredSubject.objects.get(
            identity=maternal_consent.identity
        )
        SpecimenConsent.objects.create(
            registered_subject=registered_subject,
            consent_datetime=timezone.now(),
            may_store_samples=YES,
        )
        self.assertEqual(OutgoingTransaction.objects.filter(tx_name='td_maternal.maternalconsent').count(), 1)

    def test_speciman_consent_deserialize(self):
        """ Serialized specimenconsent record should be able deserialized. """
        maternal_eligibility = MaternalEligibilityFactory()
        maternal_consent = MaternalConsentFactory(
            maternal_eligibility=maternal_eligibility
        )
        registered_subject = RegisteredSubject.objects.get(
            identity=maternal_consent.identity
        )
        specimen_consent = SpecimenConsent.objects.create(
            registered_subject=registered_subject,
            consent_datetime=timezone.now(),
            may_store_samples=YES,
            is_literate=YES
        )
        outgoing_tx = OutgoingTransaction.objects.get(tx_name='td_maternal.specimenconsent')
        deserialized_obj = serializers.deserialize(
            "json", self.aes_decrypt(outgoing_tx.tx),
            use_natural_foreign_keys=True, use_natural_primary_keys=True)
        self.assertEqual(specimen_consent.pk, deserialized_obj.pk)
