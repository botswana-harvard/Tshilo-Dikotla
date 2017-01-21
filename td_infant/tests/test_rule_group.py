from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from edc_constants.constants import SCREENED
from edc_registration.models import RegisteredSubject
from edc_identifier.models import SubjectIdentifier
from edc_constants.constants import (
    FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, UNKEYED, POS, NEG, YES, NO, NOT_APPLICABLE, UNKNOWN, NEW)
from edc_meta_data.models import RequisitionMetaData, CrfMetaData
from edc_appointment.models import Appointment

from tshilo_dikotla.constants import NO_MODIFICATIONS, DISCONTINUED, NEVER_STARTED
from td_maternal.tests import BaseTestCase
from td_maternal.models import MaternalVisit

from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabourDelFactory,
                                         MaternalVisitFactory)
from .factories import (InfantBirthFactory, InfantVisitFactory, InfantArvProphFactory, InfantBirthArvFactory,
                        InfantBirthDataFactory, InfantFuFactory, InfantFuDxFactory)


class TestRuleGroups(BaseTestCase):

    def setUp(self):
        super(TestRuleGroups, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

    def test_congentinal_yes(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        infant_birth_factory = InfantBirthDataFactory(infant_visit=self.infant_visit, congenital_anomalities=YES)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantcongenitalanomalies',
                appointment=self.appointment).count(), 1)

    def test_congentinal_no(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        infant_birth_factory = InfantBirthDataFactory(infant_visit=self.infant_visit, congenital_anomalities=NO)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantcongenitalanomalies',
                appointment=self.appointment).count(), 0)
    
    def test_infantfu_assessment_yes(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        InfantFuFactory(infant_visit=self.infant_visit, physical_assessment=YES)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantfuphysical',
                appointment=self.appointment).count(), 1)

    def test_infantfu_assessment_no(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        infantfu = InfantFuFactory(infant_visit=self.infant_visit, physical_assessment=NO)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantfuphysical',
                appointment=self.appointment).count(), 0)

    def test_infantfu_has_dx_yes(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        infantfu = InfantFuFactory(infant_visit=self.infant_visit, has_dx=YES)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantfudx',
                appointment=self.appointment).count(), 1)

    def test_infantfu_has_dx_no(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        infantfu = InfantFuFactory(infant_visit=self.infant_visit, has_dx=NO)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantfudx',
                appointment=self.appointment).count(), 0)

    def test_infant_arv_proph_required_at_2010(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantarvproph',
                appointment=self.appointment).count(), 1)

    def test_infant_arv_proph_not_required_hiv_neg_mother(self):
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
                   'rapid_test_date': date.today(),
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantarvproph',
                appointment=self.appointment).count(), 0)

    def test_infant_arv_proph_required_at_2020(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        InfantArvProphFactory(infant_visit=self.infant_visit, prophylatic_nvp=YES, arv_status=NO_MODIFICATIONS)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2020')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantarvproph',
                appointment=self.appointment).count(), 1)

    def test_infant_arv_proph_required_at_2060(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        InfantArvProphFactory(infant_visit=self.infant_visit, prophylatic_nvp=YES, arv_status=NO_MODIFICATIONS)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2020')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        InfantArvProphFactory(infant_visit=self.infant_visit, prophylatic_nvp=YES, arv_status=DISCONTINUED)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2060')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantarvproph',
                appointment=self.appointment).count(), 0)

    def test_infant_birth_arv_required_2000(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantbirtharv',
                appointment=self.appointment).count(), 1)

    def test_infant_birth_arv_not_required_2000(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': NEG,
                   'evidence_hiv_status': YES,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_date': date.today(),
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_infant',
                crf_entry__model_name='infantbirtharv',
                appointment=self.appointment).count(), 0)
