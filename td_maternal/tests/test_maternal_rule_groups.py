from dateutil.relativedelta import relativedelta
import pytz

from datetime import time, datetime

from model_mommy import mommy

from django.test import TestCase, tag

from edc_constants.constants import NEG
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata, RequisitionMetadata

from .test_mixins import PosMotherMixin, NegMotherMixin
from td.models import Appointment


@tag('review')
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
        self.add_maternal_visits('1000M')
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
        maternal_visit = self.add_maternal_visit('1010M')
        mommy.make_recipe(
            'td_maternal.maternalinterimidcc',
            maternal_visit=maternal_visit,
            recent_cd4_date=(self.get_last_maternal_visit().report_datetime - relativedelta(months=4)).date())
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
        maternal_visit = self.add_maternal_visit('1010M')
        mommy.make_recipe(
            'td_maternal.maternalinterimidcc',
            maternal_visit=maternal_visit,
            recent_cd4=15,
            recent_cd4_date=(self.get_last_maternal_visit().report_datetime - relativedelta(weeks=2)).date())
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
        '''Test NVP Dispensing required for NVP randomized mother/infant at 2000M visit.
         Using the randomized list with the third randomization being NVP'''

        # First participant
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
#         self.make_rando(rx='NVP')
        mommy.make_recipe(
            'td_maternal.maternalrando', maternal_visit=self.get_maternal_visit('1010M'))
        self.add_maternal_visits('1020M')
        self.make_delivery()
        self.add_maternal_visits('2000M')

        # Second participant
        maternal_eligibility_1 = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent_1 = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility_reference=maternal_eligibility_1.reference)
        mommy.make_recipe('td_maternal.antenatalenrollment', subject_identifier=maternal_consent_1.subject_identifier)
        appointment_1000_1 = Appointment.objects.get(
            subject_identifier=maternal_consent_1.subject_identifier, visit_code='1000M')
        maternal_visit_1000_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=appointment_1000_1, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=maternal_visit_1000_1, number_of_gestations=1)
        report_datetime = maternal_visit_1000_1.report_datetime + relativedelta(months=1)
        mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo',
            report_datetime=report_datetime,
            subject_identifier=maternal_consent_1.subject_identifier)
        appointment_1010_1 = Appointment.objects.get(
            subject_identifier=maternal_consent_1.subject_identifier, visit_code='1010M')
        antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=appointment_1010_1, reason='scheduled')
        maternal_rando_1 = mommy.make_recipe(
            'td_maternal.maternalrando', maternal_visit=antenatal_visit_1)
        self.assertEqual(maternal_rando_1.sid, 2)

        # Third participant
        maternal_eligibility_2 = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent_2 = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility_reference=maternal_eligibility_2.reference)
        mommy.make_recipe('td_maternal.antenatalenrollment', subject_identifier=maternal_consent_2.subject_identifier)
        appointment_1000_2 = Appointment.objects.get(
            subject_identifier=maternal_consent_2.subject_identifier, visit_code='1000M')
        maternal_visit_1000_2 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=appointment_1000_2, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=maternal_visit_1000_2, number_of_gestations=1)
        mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo',
            report_datetime=report_datetime,
            subject_identifier=maternal_consent_2.subject_identifier)
        appointment_1010_2 = Appointment.objects.get(
            subject_identifier=maternal_consent_2.subject_identifier, visit_code='1010M')
        antenatal_visit_2 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=appointment_1010_2, reason='scheduled')
        maternal_rando_2 = mommy.make_recipe(
            'td_maternal.maternalrando', maternal_visit=antenatal_visit_2)
        self.assertEqual(maternal_rando_2.sid, 3)
        appointment_1020_2 = Appointment.objects.get(
            subject_identifier=maternal_consent_2.subject_identifier, visit_code='1020M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=appointment_1020_2, reason='scheduled')
        delivery_datetime = pytz.utc.localize(datetime.combine(self.antenatal_enrollment.edd, time()))
        mommy.make_recipe(
            'td_maternal.maternallabdel',
            report_datetime=report_datetime,
            delivery_datetime=delivery_datetime,
            subject_identifier=maternal_consent_2.subject_identifier)

        appointment_2000_2 = Appointment.objects.get(
            subject_identifier=maternal_consent_2.subject_identifier, visit_code='2000M')
        mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=appointment_2000_2, reason='scheduled')

        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=maternal_consent_2.subject_identifier,
                entry_status=REQUIRED,
                model='td_maternal.nvpdispensing',
                visit_code='2000M').count(), 1)

    def test_nvp_dispensing_not_required_2000M_AZT(self):
        '''Test NVP Dispensing required for NVP randomized mother/infant at 2000M visit'''
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
        self.make_rando(rx='AZT')
        self.add_maternal_visits('1020M')
        self.make_delivery()
        self.add_maternal_visits('2000M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=self.subject_identifier,
                entry_status=NOT_REQUIRED,
                model='td_maternal.nvpdispensing',
                visit_code='2000M').count(), 1)


@tag('review')
class TestMaternalRuleGroupsNeg(NegMotherMixin, TestCase):

    def test_maternal_rapid_test_required_delivery(self):
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        maternal_visit = self.get_last_maternal_visit()
        self.make_delivery()
        self.make_rapid_test(
            result=NEG, result_date=(
                self.get_last_maternal_visit().report_datetime - relativedelta(days=90)).date(),
            visit=maternal_visit)
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
        """Assert ultrasound not required if filled at 1000M visit."""
        self.add_maternal_visits('1000M')
        self.make_ultrasound(self.get_maternal_visit('1000M'))
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.subject_identifier,
                model='td_maternal.maternalultrasoundinitial',
                visit_code='1010M').count(), 1)

    def test_maternal_ultra_sound_initial_required_at_1010(self):
        """Assert ultrasound required at visit 1010M if not filled at visit 1000M."""
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=self.subject_identifier,
                entry_status=REQUIRED,
                model='td_maternal.maternalultrasoundinitial',
                visit_code='1010M').count(), 1)
