from dateutil.relativedelta import relativedelta
from django.utils import timezone
from model_mommy import mommy

from edc_constants.constants import YES, NOT_APPLICABLE, POS, NO

from td.models import Appointment
from td.models import RegisteredSubject
from td_maternal.forms import MaternalArvPregForm, MaternalArvForm

from .base_test_case import BaseTestCase


class TestMaternalArvPregForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalArvPregForm, self).setUp()
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitail', maternal_visit=self.maternal_visit_1000, number_of_gestations=1,)

        self.options = {
            'maternal_visit': self.maternal_visit_1000,
            'report_datetime': timezone.now(),
            'took_arv': YES,
            'is_interrupt': NO,
            'interrupt': 'N/A',
            'interrupt_other': '',
            'comment': ''}

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
        maternal_arv_preg = mommy.make_recipe('td_maternal.maternalarvpreg', maternal_visit=self.maternal_visit_1000)
        inline_data = {
            'maternal_arv_preg': maternal_arv_preg.id,
            'arv_code': '3TC',
            'start_date': timezone.now().date() - timezone.timedelta(days=1),
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
        maternal_arv_preg = mommy.make_recipe('td_maternal.maternalarvpreg', maternal_visit=self.maternal_visit_1000, took_arv=YES)
        maternalarvhistory = mommy.make_recipe(
            'td_maternal.maternalArvhistory',
            maternal_visit=self.maternal_visit_1000,
            haart_start_date=(timezone.datetime.now() - relativedelta(weeks=9)).date())
        inline_data = {
            'maternal_arv_preg': maternal_arv_preg.id,
            'arv_code': 'Zidovudine',
            'start_date': timezone.now().date() - timezone.timedelta(weeks=10),
            'stop_date': timezone.now().date()
        }
        form = MaternalArvForm(data=inline_data)
        self.assertIn(
            "Your ARV start date {} in this pregnancy cannot be before your "
            "Historical ARV date {}".format(inline_data['start_date'], maternalarvhistory.haart_start_date),
            form.errors.get('__all__'))
