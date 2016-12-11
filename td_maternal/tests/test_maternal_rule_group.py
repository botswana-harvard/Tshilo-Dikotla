from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from django.test.testcases import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import NEG, YES
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata, RequisitionMetadata

from .test_mixins import PosMotherMixin, NegMotherMixin


class TestMaternalRuleGroupsPos(PosMotherMixin, TestCase):

    def test_maternal_hiv_maternalrando(self):
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.subject_identifier,
                model='td_maternal.maternalrando',
                visit_code='1010M').count(), 1)

    def test_maternal_hiv_maternal_lifetime_arv_history(self):
        """Assert maternallifetimearvhistory is required for POS at 1000M."""
        self.add_maternal_visits('1000M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.subject_identifier,
                model='td_maternal.maternallifetimearvhistory',
                visit_code='1000M').count(), 1)

    def test_maternal_hiv_maternal_interim_idcc(self):
        """Assert maternalinterimidcc is required for POS at 1010M."""
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.subject_identifier,
                model='td_maternal.maternalinterimidcc',
                visit_code='1010M').count(), 1)

    def test_maternal_cd4_required_recent_grt_3months(self):
        """Test that CD4 requisition is required for all POS is recent CD4 > 3months."""
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        maternal_visit = self.add_maternal_visits('1010M')
        mommy.make_recipe(
            'td_maternal.maternalinterimidcc',
            maternal_visit=maternal_visit,
            recent_cd4_date=(get_utcnow() - relativedelta(months=4)).date())
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.subject_identifier,
                model='td_lab.maternalrequisition',
                panel_name='CD4',
                visit_code='1010M').count(), 1)

    def test_maternal_cd4_not_required_recent_lt_3months(self):
        """Test that CD4 requisition not required for all POS if recent CD4 < 3months."""
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        maternal_visit = self.add_maternal_visits('1010M')
        mommy.make_recipe(
            'td_maternal.maternalinterimidcc',
            maternal_visit=maternal_visit,
            recent_cd4=15,
            recent_cd4_date=(get_utcnow() - relativedelta(weeks=2)).date())
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.subject_identifier,
                model='td_lab.maternalrequisition',
                panel_name='CD4',
                visit_code='1010M').count(), 1)

    def test_maternal_pbmc_pl_not_req_hiv_pos(self):
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.subject_identifier,
                model='td_lab.maternalrequisition',
                panel_name='PBMC Plasma (STORE ONLY)',
                visit_code='1010M').count(), 1)

    def test_nvp_dispensing_required_2000M_NVP(self):
        '''Test NVP Dispensing required for NVP randomized mother/infant at 2000M visit'''
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        maternal_visit = self.add_maternal_visits('1010M')
        mommy.make_recipe(
            'td_maternal.maternalrando',
            maternal_visit=maternal_visit,
            rx='NVP')
        self.add_maternal_visits('1020M')
        mommy.make_recipe(
            'td_maternal.maternallabdel', subject_identifier=self.subject_identifier)
        self.add_maternal_visits('2000M')
        maternal_visit = self.get_maternal_visit('2000M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=self.subject_identifier,
                entry_status=REQUIRED,
                model='td_maternal.nvpdispensing',
                visit_code='2000M').count(), 1)

    def test_nvp_dispensing_not_required_2000M_AZT(self):
        '''Test NVP Dispensing required for NVP randomized mother/infant at 2000M visit'''
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        maternal_visit = self.add_maternal_visits('1010M')
        mommy.make_recipe(
            'td_maternal.maternalrando',
            maternal_visit=maternal_visit,
            rx='AZT')
        self.add_maternal_visits('1020M')
        mommy.make_recipe(
            'td_maternal.maternallabdel', subject_identifier=self.subject_identifier)
        self.add_maternal_visits('2000M')
        maternal_visit = self.get_maternal_visit('2000M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=self.subject_identifier,
                entry_status=NOT_REQUIRED,
                model='td_maternal.nvpdispensing',
                visit_code='2000M').count(), 1)


class TestMaternalRuleGroupsNeg(NegMotherMixin, TestCase):

    def test_maternal_rapid_test_required_delivery(self):
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        maternal_visit = self.get_last_maternal_visit()
        self.make_delivery()
        self.make_rapid_test(
            result=NEG, result_date=(get_utcnow() - relativedelta(days=90)).date(), visit=maternal_visit)
        maternal_visit = self.add_maternal_visit('2000M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=self.subject_identifier,
                entry_status=REQUIRED,
                model='td_maternal.rapidtestresult',
                visit_code='2000M').count(), 1)

    def test_maternal_required_pbmc_pl_hiv_neg(self):
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.subject_identifier,
                model='td_lab.maternalrequisition',
                panel_name='PBMC Plasma (STORE ONLY)',
                visit_code='1010M').count(), 1)

    def test_maternal_ultra_sound_initial_not_required_at_1010(self):
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.subject_identifier,
                model='td_lab.maternalrequisition',
                visit_code='1010M').count(), 0)

    def test_maternal_ultra_sound_initial_required_at_1010(self):
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=self.subject_identifier,
                entry_status=NOT_REQUIRED,
                model='td_maternal.maternalultrasoundinitial',
                visit_code='1010M').count(), 1)
