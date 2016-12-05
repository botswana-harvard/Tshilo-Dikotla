from dateutil.relativedelta import relativedelta
from django.utils import timezone
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import (YES, NOT_APPLICABLE, POS, NO)
from edc_registration.models import RegisteredSubject

from td.models import Appointment

from ..forms import MaternalArvPostForm

from .base_test_case import BaseTestCase


class TestMaternalArvPost(BaseTestCase):

    def setUp(self):
        super(TestMaternalArvPost, self).setUp()

        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('subject_identifier'), visit_code='1020M')

        mommy.make_recipe('td_maternal.maternallabourdel', subject_identifier=self.options.get('subject_identifier'))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('subject_identifier'), visit_code='2000M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.options.get('subject_identifier'), visit_code='2010M')
        self.maternal_visit_2000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.data = {
            'maternal_visit': self.maternal_visit_2000.id,
            'report_datetime': get_utcnow(),
            'on_arv_since': NO,
            'on_arv_reason': 'N/A',
            'on_arv_reason_other': '',
            'arv_status': 'N/A'}

    def test_on_haart_1(self):
        """Assert that if mother was supposed to take HAART,
        then reason for haart cannot be N/A"""
        self.data.update(on_arv_since=YES)
        form = MaternalArvPostForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("You indicated that participant was on triple ARVs. Reason CANNOT be"
                      " 'Not Applicable'. ", errors)

    def test_on_haart_2(self):
        """Assert that if mother was not supposed to take HAART, then cannot provide
        a reason for taking HAART"""
        self.data.update(on_arv_reason='pmtct bf')
        form = MaternalArvPostForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that participant was not on HAART. You CANNOT provide a reason.', errors)

    def test_on_haart_3(self):
        """Assert that mother was not supposed to take HAART and no reason for taking HAART
        is provided then valid"""
        form = MaternalArvPostForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_on_haart_4(self):
        """Assert that if mother was supposed to take HAART, and reason for HAART given is valid"""
        self.data.update(
            on_arv_since=YES,
            on_arv_reason='pmtct bf')
        form = MaternalArvPostForm(data=self.data)
        self.assertTrue(form.is_valid())
