from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from django.test.testcases import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import (POS, NEG, YES, NO, NOT_APPLICABLE)
from edc_metadata.constants import REQUIRED
from edc_metadata.models import CrfMetadata, RequisitionMetadata

from td.models import Appointment

from ..models import MaternalVisit


class TestMaternalRuleGroups(TestCase):

    def setUp(self):
        super(TestMaternalRuleGroups, self).setUp()
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

    def test_maternal_hiv_maternalrando(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status='REQUIRED',
                subject_identifier=self.registered_subject.subject_identifier,
                model='td_maternal.maternalrando',
                visit_code='1010M').count(), 1)

    def test_maternal_hiv_maternal_lifetime_arv_history(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.registered_subject.subject_identifier,
                model='td_maternal.maternallifetimearvhistory',
                visit_code='1000M').count(), 1)

    def test_maternal_hiv_maternal_interim_idcc(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership', 
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status='REQUIRED',
                subject_identifier=self.registered_subject.subject_identifier,
                model='td_maternal.maternalinterimidcc',
                visit_code='1010M').count(), 1)

    def test_maternal_cd4_required_recent_grt_3months(self):
        """Test that CD4 requisition is required for all POS is recent CD4 > 3months."""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.maternalinterimidcc',
            maternal_visit=self.antenatal_visit_1,
            recent_cd4_date=(get_utcnow() - relativedelta(months=4)).date())

        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.registered_subject.subject_identifier,
                model='td_lab.maternalrequisition',
                panel_name='CD4').count(), 1)

    def test_maternal_cd4_not_required_recent_lt_3months(self):
        """Test that CD4 requisition is required for all POS if recent CD4 > 3months."""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.assertTrue(MaternalVisit.objects.all().count(), 2)
        mommy.make_recipe(
            'td_maternal.maternalinterimidcc',
            maternal_visit=self.antenatal_visit_1, recent_cd4=15,
            recent_cd4_date=(get_utcnow() - relativedelta(weeks=2)).date())
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.registered_subject.subject_identifier,
                model='td_lab.maternalrequisition',
                panel_name='CD4',
                visit_code='1010M').count(), 0)

    def test_maternal_rapid_test_required_delivery(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': YES,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_date': get_utcnow().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}

        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.antenatal_visit_2 = mommy.make_recipe(
            'td_maternal.maternalvisit',
            appointment=Appointment.objects.get(subject_identifier=options.get('registered_subject'),
                                                visit_code='1020M'), reason='scheduled')
        self.maternal_labour_del = mommy.make_recipe(
            'td_maternal.maternallabdel',
            registered_subject=options.get('registered_subject'),
            live_infants_to_register=1)
        mommy.make_recipe(
            'td_maternal.rapidtestresult',
            maternal_visit=self.antenatal_visit_2, rapid_test_done=YES, result=NEG,
            result_date=(get_utcnow() - relativedelta(days=90)).date())

        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'),
            visit_code='2000M')
        self.maternal_visit_2000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=options.get('registered_subject'),
                entry_status=REQUIRED,
                model='td_maternal.rapidtestresult',
                visit_code='2000M').count(), 1)

    def test_maternal_pbmc_pl_not_req_hiv_pos(self):
        """"""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status='REQUIRED',
                subject_identifier=self.registered_subject.subject_identifier,
                model='td_lab.maternalrequisition',
                panel_name='PBMC Plasma (STORE ONLY)').count(), 0)

    def test_maternal_required_pbmc_pl_hiv_neg(self):
        """"""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': YES,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_date': get_utcnow().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status='REQUIRED',
                subject_identifier=self.registered_subject.subject_identifier,
                model='td_lab.maternalrequisition',
                panel_name='PBMC Plasma (STORE ONLY)',
                visit_code='1010M').count(), 1)

    def test_maternal_ultra_sound_initial_not_required_at_1010(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': YES,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_date': get_utcnow().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}

        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.registered_subject.subject_identifier,
                model='td_lab.maternalrequisition', visit_code='1010M').count(), 0)

    def test_maternal_ultra_sound_initial_required_at_1010(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': YES,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_date': get_utcnow().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}

        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=self.registered_subject.subject_identifier,
                entry_status=REQUIRED,
                model='td_maternal.maternalultrasoundinitial',
                visit_code='1010M').count(), 0)

    def test_nvp_dispensing_required_2000M(self):
        '''Test NVP Dispensing required for NVP randomized mother/infant at 2000M visit'''
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)

        """Second participant"""
        self.maternal_eligibility_2 = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent_2 = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility_2,
            first_name='TATAS', last_name='TATAS', identity="111121113", confirm_identity="111121113")
        self.registered_subject_2 = self.maternal_consent_2.maternal_eligibility.registered_subject

        options = {'registered_subject': self.registered_subject_2,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)
        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=self.registered_subject_2)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        maternal_rando_2 = mommy.make_recipe(
            'td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)
        self.assertEqual(maternal_rando_2.sid, 2)

        """Third participant"""
        self.maternal_eligibility_3 = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent_3 = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility_3,
            first_name='TATAR', last_name='TATAR', identity="111121113", confirm_identity="111121113")
        self.registered_subject_3 = self.maternal_consent_3.maternal_eligibility.registered_subject

        options = {'registered_subject': self.registered_subject_3,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_3.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)
        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=self.registered_subject_3)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_3.subject_identifier, visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        maternal_rando_3 = mommy.make_recipe(
            'td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)
        self.assertEqual(maternal_rando_3.sid, 3)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_3.subject_identifier, visit_code='1020M')

        mommy.make_recipe(
            'td_maternal.maternallabdel', registered_subject=self.registered_subject_3)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_3.subject_identifier, visit_code='2000M')
        mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=self.registered_subject_3.subject_identifier,
                entry_status=REQUIRED,
                model='td_maternal.nvpdispensing',
                visit_code='2000M').count(), 1)

    def test_nvp_dispensing_not_required_2000M(self):
        '''Test NVP Dispensing not required for AZT randomized mother/infant at 2000M visit'''
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership',
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')

        mommy.make_recipe(
            'td_maternal.maternallabdel', registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=self.registered_subject.subject_identifier,
                entry_status=REQUIRED,
                model='td_maternal.nvpdispensing',
                visit_code='2000M').count(), 0)
