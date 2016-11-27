from django.test.testcases import TestCase

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import date
from model_mommy import mommy

from edc_constants.constants import (YES, NEG, NOT_APPLICABLE, POS, NO)
from td.models import Appointment


class BaseTestCase(TestCase):

    def setUp(self):
        self.study_site = '40'

    def create_mother(self, options):
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalenrollment', registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')
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
        return options
