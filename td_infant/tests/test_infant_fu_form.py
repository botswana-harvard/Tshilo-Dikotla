from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_constants.constants import POS, YES, NO, NOT_APPLICABLE
from td.models import Appointment

from td_maternal.tests import BaseTestCase
from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabourDelFactory,
                                         MaternalVisitFactory)
from td_infant.forms import InfantFuForm
from .factories import InfantBirthFactory, InfantVisitFactory


class TestInfantFu(BaseTestCase):

    def setUp(self):
        super(TestInfantFu, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
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

        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject)

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

        self.infant_visit = InfantVisitFactory(appointment=self.appointment, reason='scheduled')
        self.options = {
            'report_datetime': timezone.now(),
            'infant_birth': self.infant_birth.id,
            'infant_visit': self.infant_visit.id,
            'physical_assessment': NO,
            'diarrhea_illness': NO,
            'has_dx': NO,
            'was_hospitalized': NO,
        }

    def test_infant_hospitalization(self):
        self.options['infant_birth'] = self.infant_visit.id
        self.options['was_hospitalized'] = YES
        infant_fu = InfantFuForm(data=self.options)
        self.assertIn(
            'If infant was hospitalized, please provide # of days hospitalized',
            infant_fu.errors.get('__all__'))

    def test_validate_hospitalization_duration(self):
        self.options['infant_birth'] = self.infant_visit.id
        self.options['was_hospitalized'] = YES
        self.options['days_hospitalized'] = 100
        infant_fu = InfantFuForm(data=self.options)
        self.assertIn(
            'days hospitalized cannot be greater than 90days',
            infant_fu.errors.get('__all__'))
