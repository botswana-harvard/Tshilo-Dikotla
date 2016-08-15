from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_constants.constants import (UNKNOWN, 
    YES, NEG, NOT_APPLICABLE, POS, NO, SCHEDULED, CONTINUOUS, STOPPED, RESTARTED)

from td_list.models import PriorArv
from td_maternal.models import MaternalVisit, RegisteredSubject
from td_maternal.forms import MaternalArvPregForm, MaternalArvForm

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalVisitMembershipFactory, MaternalRandomizationFactory,
                        MaternalVisitFactory, MaternalArvPregFactory, MaternalArvHistoryFactory)


class TestMaternalArvPregForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalArvPregForm, self).setUp()
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
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'took_arv': YES,
            'is_interrupt': NO,
            'interrupt': 'N/A',
            'interrupt_other': '',
            'comment': '',}

#     def test_valid_regimen_but_no_arv(self):
#             """Assert that Enrollment shows participant on valid_regimen but now says
#             did not take arv"""
#             self.options['took_arv'] = NO
#             self.postnatal_enrollment.valid_regimen_duration = YES
#             self.postnatal_enrollment.save()
#             form = MaternalArvPregForm(data=self.options)
#             errors = ''.join(form.errors.get('__all__'))
#             self.assertIn(
#                 "At PNT you indicated that the participant has been on regimen for period of time. "
#                 "But now you indicated that the participant did not take ARVs. "
#                 "Please Correct.", errors)

    def test_medication_interrupted(self):
        """Assert that ARV indicated as interrupted, then reason expected"""
        self.options['is_interrupt'] = YES
        form = MaternalArvPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that ARVs were interrupted during pregnancy. '
                      'Please provide a reason', errors)

    def test_no_interruption_reason_given(self):
        """Assert that ARV indicated as not interrupted, then reason not expected"""
        self.options['interrupt'] = 'FORGOT'
        form = MaternalArvPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that ARVs were NOT interrupted during pregnancy. '
                      'You cannot provide a reason.', errors)

    def test_took_arv(self):
        """Assert arv taken but none listed"""
        maternal_arv_preg = MaternalArvPregFactory(maternal_visit = self.maternal_visit)
        inline_data = {
            'maternal_arv_preg': maternal_arv_preg.id,
            'arv_code': '3TC', 
            'start_date':timezone.now().date() - timezone.timedelta(days=1),
            'stop_date': timezone.now().date()
        }
        form = MaternalArvForm(data=inline_data)
        self.assertIn(
            "You indicated that participant started ARV(s) during this "
            "pregnancy. Please list them on 'Maternal ARV' table", form.errors.get('__all__'))

    def test_start_stop_date(self):
        """Assert you cannot put a stop date that is before the start date"""
        self.options['arv_code'] = '3TC'
        self.options['start_date'] = timezone.now().date()
        self.options['stop_date'] = timezone.now().date() - timezone.timedelta(days=1)
        form = MaternalArvForm(data=self.options)
        self.assertIn(
            'Your stop date of {} is prior to start date of {}. '
            'Please correct'.format(
                self.options['stop_date'], self.options['start_date']), form.errors.get('__all__'))

    def test_validate_historical_and_present_arv_start_dates(self):
        """"""
        maternal_arv_preg = MaternalArvPregFactory(maternal_visit = self.maternal_visit, took_arv=YES)
        maternalarvhistory = MaternalArvHistoryFactory(
            maternal_visit=self.maternal_visit, haart_start_date=(timezone.datetime.now() - relativedelta(weeks=9)).date())
        inline_data = {
            'maternal_arv_preg': maternal_arv_preg.id,
            'arv_code': 'Zidovudine', 
            'start_date':timezone.now().date() - timezone.timedelta(weeks=10),
            'stop_date': timezone.now().date()
        }
        form = MaternalArvForm(data=inline_data)
        self.assertIn(
            "Your ARV start date {} in this pregnancy cannot be before your "
            "Historical ARV date {}".format(
            inline_data['start_date'], maternalarvhistory.haart_start_date), form.errors.get('__all__'))
