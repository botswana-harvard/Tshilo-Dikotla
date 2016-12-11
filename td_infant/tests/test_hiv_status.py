from django.test.testcases import TestCase

from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_metadata.models import RequisitionMetadata

from td_maternal.tests.test_mixins import DeliverMotherMixin, CompleteMaternalCrfsMixin, PosMotherMixin

from .test_mixins import AddVisitInfantMixin, InfantBirthMixin


class TestHivStatus(InfantBirthMixin, DeliverMotherMixin, AddVisitInfantMixin, CompleteMaternalCrfsMixin,
                    PosMotherMixin, TestCase):

    def test_dnapcr_for_non_heu_infant(self):
        """Asserts if NON HEU infant DNA PCR requisition is NOT made available."""
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                model='td_lab.infantrequisition',
                panel_name='DNA PCR',
                visit_code='2010').count(), 1)

    def test_dnapcr_for_exposed_infant(self):
        """Asserts that DNA PCR requisition is made available for an HIV exposed infant.
        """
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status=REQUIRED,
                model='td_lab.infantrequisition',
                panel_name='DNA PCR',
                visit_code='2010').count(), 1)
