from dateutil.relativedelta import relativedelta
from datetime import timedelta
from django.utils import timezone

from edc_constants.constants import UNKNOWN, YES, NEG, NOT_APPLICABLE, POS, NO, SCHEDULED
from edc_registration.models import RegisteredSubject

from td_maternal.models import MaternalVisit
from td_maternal.forms import MaternalObstericalHistoryForm

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory)


class TestMaternalObstericalHistoryForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalObstericalHistoryForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'knows_lmp': NO,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=20)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,
            est_edd_ultrasound = timezone.now().date() + timedelta(days=120), ga_confrimation_method=1)

        self.options = {
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit.id,
            'prev_pregnancies': 1,
            'pregs_24wks_or_more': 0,
            'lost_before_24wks': 0,
            'lost_after_24wks': 0,
            'live_children': 0,
            'children_died_b4_5yrs': 0,
            'children_deliv_before_37wks': 0,
            'children_deliv_aftr_37wks': 0
        }

    def test_maternal_obsterical_less_than_24_wks_ga_prev_preg_1(self):
        self.options['lost_after_24wks'] = 1
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertIn(
            'You indicated previous pregancies were {}. Number of pregnancies at or after 24 weeks, '
            'number of living children, number of children lost after 24 '
            'weeks should all be zero.'.format(self.options['prev_pregnancies']), mob_form.errors.get('__all__'))

    def test_maternal_obsterical_less_than_24_wks_ga_prev_preg_more_than_1(self):
        self.options['prev_pregnancies'] = 3
        self.options['lost_before_24wks'] = 2
        self.options['lost_after_24wks'] = 2
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertIn(
            'The sum of Q3, Q4, Q5, Q6 and Q7 must all add up to Q2 - 1. Please correct.'.format(self.options['prev_pregnancies']),
            mob_form.errors.get('__all__'))

    def test_maternal_obsterical_24wks_or_more_pregnancy(self):
        self.options['prev_pregnancies'] = 3
        self.options['lost_before_24wks'] = 2
        self.options['lost_after_24wks'] = 2
        self.maternal_ultrasound.est_edd_ultrasound = timezone.now().date() + timedelta(days=90)
        self.maternal_ultrasound.save()
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertIn(
            'The sum of Q3, Q4, Q5, Q6 and Q7 must be equal to Q2. Please correct.'.format(self.options['prev_pregnancies']),
            mob_form.errors.get('__all__'))
