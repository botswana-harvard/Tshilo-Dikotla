from dateutil.relativedelta import relativedelta
from model_mommy import mommy
from django.test import TestCase
from django.utils import timezone

from edc_base.utils import get_utcnow
from edc_pregnancy_utils.constants import ULTRASOUND

from ..models import MaternalLabDel
from ..pregnancy import Pregnancy

from .test_mixins import AddVisitMotherMixin, PosMotherMixin, DeliverMotherMixin


class TestPregnancy(DeliverMotherMixin, AddVisitMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestPregnancy, self).setUp()
        self.add_maternal_visit('1000M')

    def test_basics(self):
        maternal_visit = self.get_maternal_visit('1000M')
        est_edd = (timezone.now() + relativedelta(weeks=20)).date()
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            est_edd_ultrasound=est_edd,
            ga_by_ultrasound_wks=20,
            ga_by_ultrasound_days=4)
        pregnancy = Pregnancy(
            self.subject_identifier,
            reference_datetime=get_utcnow())
        self.assertEqual(pregnancy.ga_by_lmp, 25)
        self.assertEqual(pregnancy.ga.weeks, 20)
        self.assertIsNone(pregnancy.delivery_datetime)
        self.assertEqual(pregnancy.edd.edd.date(), est_edd)
        self.assertEqual(pregnancy.edd.method, ULTRASOUND)

    def test_reference_datetime_before_delivery(self):
        """Asserts ignores delivery if reference datetime before delivery datetime."""
        maternal_visit = self.get_maternal_visit('1000M')
        est_edd = (timezone.now() + relativedelta(weeks=20))
        delivery_datetime = (timezone.now() + relativedelta(weeks=20) + relativedelta(days=6))
        reference_datetime = (timezone.now() + relativedelta(weeks=19))
        maternal_lab_del = MaternalLabDel.objects.get(subject_identifier=self.subject_identifier)
        maternal_lab_del.delivery_datetime = delivery_datetime
        maternal_lab_del.save()
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            est_edd_ultrasound=est_edd.date(),
            ga_by_ultrasound_wks=20,
            ga_by_ultrasound_days=4)
        pregnancy = Pregnancy(
            self.subject_identifier,
            reference_datetime=reference_datetime)
        self.assertEqual(pregnancy.ga_by_lmp, 25)
        self.assertEqual(pregnancy.ga.weeks, 20)
        self.assertIsNone(pregnancy.delivery_datetime)
        self.assertEqual(pregnancy.edd.edd.date(), est_edd)
        self.assertEqual(pregnancy.edd.method, ULTRASOUND)
