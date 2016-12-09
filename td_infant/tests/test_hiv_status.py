from django.test.testcases import TestCase
from edc_metadata.models import RequisitionMetadata


class TestHivStatus(TestCase):

    def test_dnapcr_for_non_heu_infant(self):
        """test that for a NON HEU infant, then the DNA PCR requisition is NOT made available."""
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status='NOT_REQUIRED',
                model='td_lab.infantrequisition',
                panel_name='DNA PCR',
                visit_code='2010').count(), 1)
