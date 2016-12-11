from dateutil.relativedelta import relativedelta

from django.test.testcases import TestCase
from django.utils import timezone

from edc_base.utils import get_utcnow

from ..forms import MaternalObstericalHistoryForm

from .test_mixins import PosMotherMixin


class TestMaternalObstericalHistoryForm(PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalObstericalHistoryForm, self).setUp()

        self.options = {
            'report_datetime': get_utcnow(),
            'maternal_visit': self.get_maternal_visit('1000M').id,
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
        self.options.update(lost_after_24wks=1)
        self.maternal_ultrasound.ga_confirmed = 20
        self.maternal_ultrasound.save()
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertIn(
            'You indicated previous pregancies were {}. Number of pregnancies at or after 24 weeks, '
            'number of living children, number of children lost after 24 '
            'weeks should all be zero.'.format(self.options['prev_pregnancies']), mob_form.errors.get('__all__'))

    def test_maternal_obsterical_less_than_24_wks_ga_prev_preg_more_than_1(self):
        self.options.update(
            prev_pregnancies=3,
            lost_before_24wks=2,
            lost_after_24wks=2)
        self.maternal_ultrasound.ga_confirmed = 20
        self.maternal_ultrasound.save()
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertIn(
            'The sum of Q3, Q4 and Q5 must all add up to Q2 - 1. Please correct.'.format(self.options['prev_pregnancies']),
            mob_form.errors.get('__all__'))

    def test_maternal_obsterical_24wks_or_more_pregnancy(self):
        self.options.update(
            prev_pregnancies=3,
            lost_before_24wks=2,
            lost_after_24wks=2)
        self.maternal_ultrasound.ga_by_ultrasound_wks = 27
        self.maternal_ultrasound.est_edd_ultrasound = timezone.now() + relativedelta(weeks=13)
        self.maternal_ultrasound.save()
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertIn(
            'The sum of Q3, Q4 and Q5 must be equal to Q2. Please correct.',
            mob_form.errors.get('__all__'))

    def test_maternal_obsterical_live_children(self):
        self.options.update(
            prev_pregnancies=6,
            pregs_24wks_or_more=4,
            lost_before_24wks=1,
            lost_after_24wks=0,
            live_children=0,
            children_died_b4_5yrs=0,
            children_deliv_before_37wks=2,
            children_deliv_aftr_37wks=3)
        self.maternal_ultrasound.est_edd_ultrasound = timezone.now() + relativedelta(weeks=20)
        self.maternal_ultrasound.save()
        mob_form = MaternalObstericalHistoryForm(data=self.options)
        self.assertIn(
            'The sum of Q8 and Q9 must be equal to (Q2 -1) - (Q4 + Q5). Please correct.'.format(self.options['prev_pregnancies']),
            mob_form.errors.get('__all__'))
