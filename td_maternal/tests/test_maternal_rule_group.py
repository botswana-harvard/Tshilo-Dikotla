from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_constants.constants import SCREENED
from edc_constants.constants import (
    FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, UNKEYED, POS, YES, NO, NOT_APPLICABLE, UNK, NEW)
from edc_meta_data.models import RequisitionMetaData, CrfMetaData
from edc_appointment.models import Appointment

from td_maternal.tests import BaseTestCase
from td_maternal.models import MaternalVisit

from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalVisitFactory)


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
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__registered_subject=options.get('registered_subject'),
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit_1000,
                                                                number_of_gestations=1,
                                                                )
        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                   visit_definition__code='1010M')
        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_maternal',
                crf_entry__model_name='maternalrando',
                appointment=self.appointment).count(), 1)

    def test_maternal_hiv_maternallifetimearvhistory(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__registered_subject=options.get('registered_subject'),
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit_1000,
                                                                number_of_gestations=1,
                                                                )
        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                   visit_definition__code='1010M')
        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_maternal',
                crf_entry__model_name='maternalinterimidcc',
                appointment=self.appointment).count(), 1)

    def test_maternal_hiv_maternallifetimearvhistory_2(self):
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__registered_subject=options.get('registered_subject'),
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit_1000,
                                                                number_of_gestations=1,
                                                                )
        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                   visit_definition__code='1010M')
        self.antenatal_visit_1 = MaternalVisitFactory(appointment=self.appointment)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='td_maternal',
                crf_entry__model_name='maternalinterimidcc',
                appointment=self.appointment).count(), 1)
