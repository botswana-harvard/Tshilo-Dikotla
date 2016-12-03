from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from model_mommy import mommy

from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE
from edc_constants.constants import UNKNOWN

from td.models import Appointment
from td_list.models import RandomizationItem
from edc_registration.models import RegisteredSubject
from td.constants import RANDOMIZED

from .base_test_case import BaseTestCase


class TestMaternalRandomization(BaseTestCase):

    def setUp(self):
        super(TestMaternalRandomization, self).setUp()
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

    def test_verify_hiv_status(self):
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        with self.assertRaises(ValidationError):
            mommy.make_recipe('td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)

    def test_already_randomized(self):
        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        mommy.make_recipe('td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)
        with self.assertRaises(IntegrityError):
            mommy.make_recipe('td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)

    def test_pick_correct_next_randomization_item(self):
        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        maternal_rando = mommy.make_recipe('td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)
        self.assertEqual(maternal_rando.sid, 1)
        self.maternal_eligibility_2 = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent_2 = mommy.make_recipe(
            'td_maternal.maternalconsent', 
            maternal_eligibility=self.maternal_eligibility_2,
            first_name='TATA', last_name='TATA', identity="111121112", confirm_identity="111121112")
        self.registered_subject_2 = self.maternal_consent_2.maternal_eligibility.registered_subject

        status_options = self.hiv_pos_mother_options(self.registered_subject_2)
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **status_options)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)
        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo', registered_subject=self.registered_subject_2)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        maternal_rando_2 = mommy.make_recipe('td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)
        self.assertEqual(maternal_rando_2.sid, 2)

    def test_all_randomization_listitems_created(self):
        self.assertEqual(RandomizationItem.objects.all().count(), 300)

    def test_registered_subject_correctly_update(self):
        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        maternal_rando = mommy.make_recipe('td_maternal.maternalrandomization', maternal_visit=self.antenatal_visit_1)
        registered_subject = RegisteredSubject.objects.get(subject_identifier=maternal_rando.subject_identifier)
        self.assertEqual(registered_subject.sid, str(maternal_rando.sid))
        self.assertEqual(registered_subject.randomization_datetime, maternal_rando.randomization_datetime)
        self.assertEqual(registered_subject.registration_status, RANDOMIZED)

    def create_mother(self, status_options):
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **status_options)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)
        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo', 
            registered_subject=status_options.get('registered_subject'))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

    def hiv_pos_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        return options

    def hiv_neg_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}
        return options