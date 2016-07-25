from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_constants.constants import UNKNOWN, YES, NEG, NOT_APPLICABLE, POS, NO, SCHEDULED
from edc_registration.models import RegisteredSubject

from td_maternal.models import MaternalVisit
from td_maternal.forms import MaternalObstericalHistoryForm

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalVisitMembershipFactory, MaternalRandomizationFactory,
                        MaternalVisitFactory)


class TestMaternalObstericalHistoryForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalObstericalHistoryForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
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

        self.options = {
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit.id,
            'prev_pregnancies': 2,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 1,
            'lost_after_24wks': 1,
            'live_children': 1,
            'children_died_b4_5yrs': 1,
            'children_deliv_before_37wks': 0,
            'children_deliv_aftr_37wks': 1
        }

    def test_maternal_obsterical_history_form_valid1(self):
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertTrue(mob_form.is_valid())

    def test_maternal_obsterical_history_children_died_b4_5yrs_invalid(self):
        self.options['children_died_b4_5yrs'] = -1
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertFalse(mob_form.is_valid())

    def test_maternal_obsterical_history_children_died_b4_5yrs_valid(self):
        self.options = {
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit.id,
            'prev_pregnancies': 1,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 0,
            'lost_after_24wks': 0,
            'live_children': 1,
            'children_died_b4_5yrs': -1
        }
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertFalse(mob_form.is_valid())

    def test_maternal_obsterical_history_live_children_invalid(self):
        self.options['live_children'] = -1
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertFalse(mob_form.is_valid())

    def test_maternal_obsterical_history_live_children_valid(self):
        self.options['live_children'] = 2
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertTrue(mob_form.is_valid())

    def test_maternal_obsterical_history_pregs_24wks_or_more_invalid(self):
        self.options['pregs_24wks_or_more'] = -1
        self.options['lost_after_24wks'] = 2
        self.options['children_died_b4_5yrs'] = 2
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertFalse(mob_form.is_valid())

    def test_maternal_obsterical_history_pregs_24wks_or_more_valid(self):
        self.options['pregs_24wks_or_more'] = 1
        self.options['lost_after_24wks'] = 1
        self.options['children_died_b4_5yrs'] = 1
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertTrue(mob_form.is_valid())

    def test_zero_previous_pregnancies(self):
        self.options['prev_pregnancies'] = -1
        self.options['pregs_24wks_or_more'] = 1
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertFalse(mob_form.is_valid())

    def test_prev_pregnancies_zero(self):
        self.options['prev_pregnancies'] = 0
        self.options['pregs_24wks_or_more'] = 1
        self.options['lost_before_24wks'] = 1
        self.options['lost_after_24wks'] = 3
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertIn(u"You indicated previous pregancies were 0. Number of pregnancies at or after 24 weeks,number "
                      "of living children,number of children died after 5 year be greater than all be zero.",
                      mob_form.errors.get('__all__'))

    def test_prev_pregnancies_zero_1(self):
        self.options['prev_pregnancies'] = 1
        self.options['pregs_24wks_or_more'] = 0
        self.options['lost_before_24wks'] = 0
        self.options['lost_after_24wks'] = 0
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertIn("You indicated previous pregancies were 1. Number of pregnancies at or after 24 weeks,"
                      "number of living children,number of children died after 5 year CANNOT all be zero.",
                      mob_form.errors.get('__all__'))

#     def test_preg24wks_grt_prev_preg(self):
#         self.options['prev_pregnancies'] = 2
#         self.options['pregs_24wks_or_more'] = 3
#         mob_form = MaternalObstericalHistoryForm(data=self.options)
#         self.assertIn(
#             "Number of pregnancies carried at least 24 weeks cannot be greater than previous pregnancies.",
#             mob_form.errors.get('__all__'))

#     def test_lost_before_24wks_grt_prev_preg(self):
#         self.options['prev_pregnancies'] = 2
#         self.options['lost_before_24wks'] = 3
#         mob_form = MaternalObstericalHistoryForm(data=self.options)
#         self.assertIn(
#             "Number of pregnancies lost before 24 weeks cannot be greater than previous pregnancies.",
#             mob_form.errors.get('__all__'))

#     def test_lost_after_24wks_grt_prev_preg(self):
#         self.options['prev_pregnancies'] = 2
#         self.options['pregs_24wks_or_more'] = 1
#         self.options['lost_before_24wks'] = 1
#         self.options['lost_after_24wks'] = 3
#         mob_form = MaternalObstericalHistoryForm(data=self.options)
#         self.assertIn("Number of pregnancies lost at or after 24 weeks gestation cannot be greater "
#                       "than number of previous pregnancies or number of pregnancies at least 24 weeks.",
#                       mob_form.errors.get('__all__'))

#     def test_pregs_24wks_or_more_plus_lost_before_24wks_grt_prev_pregnancies(self):
#         self.options['prev_pregnancies'] = 3
#         self.options['pregs_24wks_or_more'] = 1
#         self.options['lost_before_24wks'] = 1
#         self.options['lost_after_24wks'] = 1
#         mob_form = MaternalObstericalHistoryForm(data=self.options)
#         self.assertIn("The sum of Number of pregnancies at least 24 weeks and "
#                       "number of pregnancies lost before 24 weeks gestation. must be equal to "
#                       "number of previous pregnancies for this participant.", mob_form.errors.get('__all__'))
