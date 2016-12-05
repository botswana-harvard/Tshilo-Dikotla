from dateutil.relativedelta import relativedelta
from datetime import date
from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_metadata.constants import REQUIRED
from edc_constants.constants import (POS, NEG, YES, NO, NOT_APPLICABLE)
from td_maternal.models import CrfMetadata

from td.models import Appointment

from td.constants import NO_MODIFICATIONS, DISCONTINUED
from td_maternal.tests import BaseTestCase
from ..models import InfantArvProph

from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabDelFactory,
                                         MaternalVisitFactory)
from .factories import (InfantBirthFactory, InfantVisitFactory, InfantArvProphFactory,
                        InfantBirthDataFactory, InfantFuFactory)


class TestRuleGroups(BaseTestCase):

    def setUp(self):
        super(TestRuleGroups, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

    def test_congentinal_yes(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        InfantBirthDataFactory(infant_visit=self.infant_visit, congenital_anomalities=YES)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantcongenitalanomalies',
                visit_code='2000').count(), 1)

    def test_congentinal_no(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        InfantBirthDataFactory(infant_visit=self.infant_visit, congenital_anomalities=NO)

        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantcongenitalanomalies',
                visit_code='2000').count(), 0)

    def test_infantfu_assessment_yes(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2010')

        self.infant_visit = InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        InfantFuFactory(infant_visit=self.infant_visit, physical_assessment=YES)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantfuphysical',
                visit_code='2010').count(), 1)

    def test_infantfu_assessment_no(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2010')

        self.infant_visit = InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        InfantFuFactory(infant_visit=self.infant_visit, physical_assessment=NO)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantfuphysical',
                visit_code='2010').count(), 0)

    def test_infantfu_has_dx_yes(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2010')

        self.infant_visit = InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        InfantFuFactory(infant_visit=self.infant_visit, has_dx=YES)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantfudx',
                visit_code='2010').count(), 1)

    def test_infantfu_has_dx_no(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2010')

        self.infant_visit = InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        InfantFuFactory(infant_visit=self.infant_visit, has_dx=NO)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantfudx',
                visit_code='2010').count(), 0)

    def test_infant_arv_proph_required_at_2010(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2010')

        InfantVisitFactory(appointment=self.appointment, reason='scheduled')

        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantarvproph',
                visit_code='2010').count(), 1)

    def test_infant_arv_proph_not_required_hiv_neg_mother(self):
        """"""
        self.options = {
            'registered_subject': self.registered_subject,
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

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2010')

        InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantarvproph',
                visit_code='2010').count(), 0)

    def test_infant_arv_proph_required_at_2020(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2010')

        self.infant_visit = InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        InfantArvProphFactory(infant_visit=self.infant_visit, prophylatic_nvp=YES, arv_status=NO_MODIFICATIONS)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2020')

        self.infant_visit = InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantarvproph',
                visit_code='2020').count(), 1)

    def test_infant_arv_proph_not_required_at_2060(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2010')

        self.infant_visit = InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        InfantArvProphFactory(infant_visit=self.infant_visit, prophylatic_nvp=YES, arv_status=NO_MODIFICATIONS)
        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2020')

        self.infant_visit = InfantVisitFactory(appointment=self.appointment, reason='scheduled')

        InfantArvProphFactory(infant_visit=self.infant_visit, prophylatic_nvp=YES, arv_status=DISCONTINUED)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2060')
        InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantarvproph',
                visit_code='2060').count(), 0)

    def test_infant_birth_arv(self):
        self.options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=self.options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')

        InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=infant_registered_subject.subject_identifier,
                model='td_infant.infantbirtharv',
                visit_code='2000').count(), 1)
