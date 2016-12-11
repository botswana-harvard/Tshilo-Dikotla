from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..forms import MaternalArvPregForm, MaternalArvForm

from .test_mixins import PosMotherMixin


@tag('postenrollment', 'forms')
class TestMaternalArvPregForm(PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalArvPregForm, self).setUp()

        maternal_visit = self.add_maternal_visit('1000M')

        self.options = {
            'maternal_visit': maternal_visit.id,
            'report_datetime': get_utcnow(),
            'took_arv': YES,
            'is_interrupt': NO,
            'interrupt': 'N/A',
            'interrupt_other': '',
            'comment': ''}

    def test_medication_interrupted(self):
        """Assert that ARV indicated as interrupted, then reason expected"""
        self.options.update(is_interrupt=YES)
        form = MaternalArvPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that ARVs were interrupted during pregnancy. '
                      'Please provide a reason', errors)

    def test_no_interruption_reason_given(self):
        """Assert that ARV indicated as not interrupted, then reason not expected"""
        self.options.update(interrupt='FORGOT')
        form = MaternalArvPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that ARVs were NOT interrupted during pregnancy. '
                      'You cannot provide a reason.', errors)

    def test_took_arv(self):
        """Assert arv taken but none listed"""
        maternal_arv_preg = mommy.make_recipe(
            'td_maternal.maternalarvpreg', maternal_visit=self.get_maternal_visit('1000M'))
        inline_data = {
            'maternal_arv_preg': maternal_arv_preg.id,
            'arv_code': '3TC',
            'start_date': (get_utcnow() - relativedelta(days=1)).date(),
            'stop_date': get_utcnow().date()
        }
        form = MaternalArvForm(data=inline_data)
        self.assertIn(
            "You indicated that participant started ARV(s) during this "
            "pregnancy. Please list them on 'Maternal ARV' table", form.errors.get('__all__'))

    def test_start_stop_date(self):
        """Assert you cannot put a stop date that is before the start date"""
        self.options.update(
            arv_code='3TC',
            start_date=get_utcnow().date(),
            stop_date=(get_utcnow() - relativedelta(days=1)).date())
        form = MaternalArvForm(data=self.options)
        self.assertIn(
            'Your stop date of {} is prior to start date of {}. '
            'Please correct'.format(
                self.options['stop_date'], self.options['start_date']), form.errors.get('__all__'))

    def test_validate_historical_and_present_arv_start_dates(self):
        """"""
        maternal_arv_preg = mommy.make_recipe(
            'td_maternal.maternalarvpreg', maternal_visit=self.get_maternal_visit('1000M'), took_arv=YES)
        maternallifetimearvhistory = mommy.make_recipe(
            'td_maternal.maternallifetimearvhistory',
            maternal_visit=self.get_maternal_visit('1000M'),
            haart_start_date=(get_utcnow() - relativedelta(weeks=9)).date())
        inline_data = {
            'maternal_arv_preg': maternal_arv_preg.id,
            'arv_code': 'Zidovudine',
            'start_date': (get_utcnow() - relativedelta(weeks=10)).date(),
            'stop_date': get_utcnow().date()
        }
        form = MaternalArvForm(data=inline_data)
        self.assertIn(
            "Your ARV start date {} in this pregnancy cannot be before your "
            "Historical ARV date {}".format(inline_data['start_date'], maternallifetimearvhistory.haart_start_date),
            form.errors.get('__all__'))
