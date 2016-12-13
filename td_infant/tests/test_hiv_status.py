from django.test import TestCase, tag

from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_metadata.models import RequisitionMetadata

from .test_mixins import InfantMixin


@tag('review')
class TestHivStatus(InfantMixin, TestCase):

    def test_dnapcr_for_non_heu_infant(self):
        """Asserts if NON HEU infant DNA PCR requisition is NOT made available."""
        self.make_infant_birth()
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
        self.make_infant_birth()
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status=REQUIRED,
                model='td_lab.infantrequisition',
                panel_name='DNA PCR',
                visit_code='2010').count(), 1)
