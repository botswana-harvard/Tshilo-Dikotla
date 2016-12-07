from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..forms import MaternalArvPostForm

from .mixins import AntenatalVisitsMotherMixin, PosMotherMixin, DeliverMotherMixin


class TestMaternalArvPost(AntenatalVisitsMotherMixin, DeliverMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalArvPost, self).setUp()

        self.add_maternal_visits('1000M', '1010M', '1020M', '2000M')
        maternal_visit = self.get_maternal_visit('2000M')

        self.data = {
            'maternal_visit': maternal_visit.id,
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
