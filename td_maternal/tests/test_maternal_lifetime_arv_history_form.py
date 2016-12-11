from datetime import date
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import (YES, NOT_APPLICABLE, NO, CONTINUOUS, STOPPED, RESTARTED)

from td_list.models import PriorArv
from td_maternal.forms import MaternalLifetimeArvHistoryForm

from .test_mixins import PosMotherMixin


class TestMaternalLifetimeArvHistoryForm(PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalLifetimeArvHistoryForm, self).setUp()
        self.maternal_visit = self.add_maternal_visit('1000M')
        prior_arv = PriorArv.objects.create(name="Atripla", short_name="Atripla")
        self.options = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': get_utcnow(),
            'haart_start_date': (get_utcnow() - relativedelta(months=9)).date(),
            'is_date_estimated': '-',
            'preg_on_haart': YES,
            'haart_changes': 0,
            'prior_preg': CONTINUOUS,
            'prior_arv': [prior_arv.id]}

    def test_arv_interrupt_1(self):
        """Assert that if was not still on ARV then 'interruption never restarted'
        is not a valid option."""
        self.options.update(
            prior_preg=STOPPED,
            haart_start_date=date(2015, 4, 10),
            preg_on_haart=YES)
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("You indicated that the mother was still on triple ARV when "
                      "she got pregnant, yet you indicated that ARVs were interrupted "
                      "and never restarted.", errors)

    def test_arv_interrupt_2(self):
        """Assert that if was not on ARV then 'Had treatment
        interruption but restarted' is not a valid option."""
        self.options.update(
            preg_on_haart=NO,
            prior_preg=RESTARTED)
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that the mother was NOT on triple ARV when she got pregnant. '
            'ARVs could not have been interrupted. Please correct.', errors)

    def test_arv_interrupt_3(self):
        """Assert that if was not still on ARV then 'Received continuous HAART from the
        time she started is not a valid option."""
        self.options.update(
            preg_on_haart=NO,
            prior_preg=CONTINUOUS)
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that the mother was NOT on triple ARV when she got pregnant. '
            'ARVs could not have been uninterrupted. Please correct.', errors)

    def test_arv_interrupt_4(self):
        """Assert that if was not still on ARV only valid answer is 'interrupted and never
        restarted'"""
        self.options.update(
            preg_on_haart=YES,
            prior_preg=STOPPED)
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        self.assertIn(
            'You indicated that the mother was still on triple ARV when she got pregnant, '
            'yet you indicated that ARVs were interrupted and never restarted. Please correct.',
            form.errors.get('__all__'))

    def test_haart_start_date_2(self):
        """Start date of ARVs CANNOT be before DOB"""
        mommy.make_recipe(
            'td_maternal.maternalobstericalhistory', maternal_visit=self.get_maternal_visit('1000M'), prev_pregnancies=1)
        self.options.update(
            prev_sdnvp_labour=NOT_APPLICABLE,
            prev_preg_azt=NOT_APPLICABLE,
            prev_preg_haart=YES,
            haart_start_date=(get_utcnow() - relativedelta(years=60)).date(),
            report_datetime=get_utcnow())
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("Date of triple ARVs first started CANNOT be before DOB.", errors)

    def test_haart_start_date_none(self):
        """Start date of ARVs CANNOT be None"""
        mommy.make_recipe(
            'td_maternal.maternalobstericalhistory', maternal_visit=self.get_maternal_visit('1000M'), prev_pregnancies=1)
        self.options.update(
            prev_sdnvp_labour=NOT_APPLICABLE,
            prev_preg_azt=NOT_APPLICABLE,
            prev_preg_haart=YES,
            haart_start_date=None,
            report_datetime=get_utcnow())
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("Please give a valid arv initiation date.", errors)

    def test_prev_preg_azt(self):
        mommy.make_recipe(
            'td_maternal.maternalobstericalhistory', maternal_visit=self.get_maternal_visit('1000M'), prev_pregnancies=0)
        self.options.update(prev_preg_azt=YES)
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'In Maternal Obsterical History form you indicated there were no previous '
            'pregnancies. Receive AZT monotherapy in previous pregancy should be '
            'NOT APPLICABLE', errors)

    def test_prev_sdnvp_labour(self):
        mommy.make_recipe(
            'td_maternal.maternalobstericalhistory', maternal_visit=self.get_maternal_visit('1000M'), prev_pregnancies=0)
        self.options.update(
            prev_sdnvp_labour=YES,
            prev_preg_azt=NOT_APPLICABLE)
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'In Maternal Obsterical History form you indicated there were no previous '
            'pregnancies. Single sd-NVP in labour during a prev pregnancy should '
            'be NOT APPLICABLE', errors)

    def test_prev_preg_haart(self):
        mommy.make_recipe(
            'td_maternal.maternalobstericalhistory', maternal_visit=self.get_maternal_visit('1000M'), prev_pregnancies=0)
        self.options.update(
            prev_sdnvp_labour=NOT_APPLICABLE,
            prev_preg_azt=NOT_APPLICABLE,
            prev_preg_haart=YES)
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'In Maternal Obsterical History form you indicated there were no previous '
            'pregnancies. triple ARVs during a prev pregnancy should '
            'be NOT APPLICABLE', errors)
