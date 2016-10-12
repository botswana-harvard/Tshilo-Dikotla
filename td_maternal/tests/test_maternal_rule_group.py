from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_constants.constants import (POS, NEG, YES, NO, NOT_APPLICABLE, UNK)
from edc_metadata.constants import NOT_REQUIRED, REQUIRED, KEYED
from edc_visit_tracking.constants import SCHEDULED
from td_appointment.models import Appointment

from td_maternal.tests import BaseTestCase
from td_maternal.models import MaternalVisit, MaternalInterimIdcc, CrfMetadata, RequisitionMetadata

from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalVisitFactory, RapidTestResultFactory,
                                         MaternalInterimIdccFactory, MaternalLabourDelFactory)


class TestMaternalRuleGroups(BaseTestCase):

    def setUp(self):
        super(TestMaternalRuleGroups, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

    def test_maternal_hiv_maternalrando(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                crf_entry__app_label='td_maternal',
                crf_entry__model_name='maternalrando').count(), 1)

    def test_maternal_hiv_maternal_lifetime_arv_history(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))

        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                crf_entry__app_label='td_maternal',
                crf_entry__model_name='maternallifetimearvhistory',
                appointment=self.appointment).count(), 1)

    def test_maternal_hiv_maternal_interim_idcc(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                crf_entry__app_label='td_maternal',
                crf_entry__model_name='maternalinterimidcc',
                appointment=self.appointment).count(), 1)

    def test_maternal_cd4_required_recent_grt_3months(self):
        """Test that CD4 requisition is required for all POS is recent CD4 > 3months."""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        MaternalInterimIdccFactory(
            maternal_visit=self.antenatal_visit_1,
            recent_cd4_date=(timezone.datetime.now() - relativedelta(months=4)).date())
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit__code='1010M')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status='REQUIRED',
                lab_entry__app_label='td_lab',
                lab_entry__model_name='maternalrequisition',
                lab_entry__requisition_panel__name='CD4',
                appointment=self.appointment).count(), 1)

    def test_maternal_cd4_not_required_recent_grt_3months(self):
        """Test that CD4 requisition is required for all POS if recent CD4 > 3months."""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(subject_identifier=options.get('registered_subject'),
                                                visit_code='1020M'), reason='scheduled')
        MaternalInterimIdccFactory(
            maternal_visit=self.antenatal_visit_2, recent_cd4=15,
            recent_cd4_date=(timezone.datetime.now() - relativedelta(weeks=2)).date())
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status='REQUIRED',
                model='maternalrequisition',
                panel_name='CD4').count(), 0)

    def test_maternal_rapid_test_required_delivery(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': YES,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_date': timezone.now().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(subject_identifier=options.get('registered_subject'),
                                                visit_code='1020M'), reason='scheduled')
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=options.get('registered_subject'),
                                                            live_infants_to_register=1)
        RapidTestResultFactory(
            maternal_visit=self.antenatal_visit_2, rapid_test_done=YES, result=NEG,
            result_date=(timezone.datetime.now() - relativedelta(days=90)).date())

        self.appointment = Appointment.objects.get(
            registered_subject=options.get('registered_subject'),
            visit_code='2000M')
        self.maternal_visit_2000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=options.get('registered_subject'),
                entry_status=REQUIRED,
                model='rapidtestresult').count(), 1)

    def test_maternal_pbmc_pl_not_req_hiv_pos(self):
        """"""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(subject_identifier=options.get('registered_subject'),
                                                visit_code='1020M'), reason='scheduled')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status='REQUIRED',
                lab_entry__app_label='td_lab',
                lab_entry__model_name='maternalrequisition',
                lab_entry__requisition_panel__name='PBMC Plasma (STORE ONLY)',
                appointment=self.appointment).count(), 0)

    def test_maternal_required_pbmc_pl_hiv_neg(self):
        """"""
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': YES,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_date': timezone.now().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(subject_identifier=options.get('registered_subject'),
                                                visit_code='1020M'), reason='scheduled')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                entry_status='REQUIRED',
                lab_entry__app_label='td_lab',
                lab_entry__model_name='maternalrequisition',
                lab_entry__requisition_panel__name='PBMC Plasma (STORE ONLY)',
                appointment=self.appointment).count(), 1)

    def test_maternal_ultra_sound_initial_not_required_at_1010(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': YES,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_date': timezone.now().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                crf_entry__app_label='td_maternal',
                crf_entry__model_name='maternalultrasoundinitial',
                appointment=self.appointment).count(), 0)

    def test_maternal_ultra_sound_initial_required_at_1010(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': YES,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_date': timezone.now().date(),
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__subject_identifier=options.get('registered_subject'),
            appointment__visit_code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                subject_identifier=options.get('registered_subject'),
                entry_status=REQUIRED,
                model='maternalultrasoundinitial',
                visit_code='1010M').count(), 1)
