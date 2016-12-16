from django.test import TestCase

from edc_constants.constants import YES, NO, NEG

from ..forms import RapidTestResultForm

from .test_mixins import NegMotherMixin, get_utcnow


class TestRapidTestForm(NegMotherMixin, TestCase):

    def setUp(self):
        super(TestRapidTestForm, self).setUp()
        self.add_maternal_visit('1000M')
        self.make_antenatal_enrollment_two()
        self.data = {
            'maternal_visit': self.add_maternal_visit('1010M').id,
            'rapid_test_done': YES,
            'result_date': get_utcnow(),
            'result': NEG}

    def test_result_date_provided(self):
        """Test if result date of the rapid test is provided"""
        self.data.update(
            rapid_test_done=YES,
            result_date=None)
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn('If a rapid test was processed, what is the date'
                      ' of the rapid test?', rapid_form.errors.get('__all__'))

    def test_rapid_test_results(self):
        """Test if the result of rapid test is provided"""
        self.data.update(
            rapid_test_done=YES,
            result_date=get_utcnow(),
            result=None)
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn('If a rapid test was processed, what is the test result?',
                      rapid_form.errors.get('__all__'))

    def test_result_date_present_no_rapid_test_result(self):
        """Test if there is a date for test and there is no test"""
        result_date = get_utcnow().date()
        self.data.update(
            rapid_test_done=NO,
            result_date=get_utcnow())
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn('If a rapid test was not processed, please do not provide the result date. '
                      'Got {}.'.format(result_date.strftime('%Y-%m-%d')), rapid_form.errors.get('__all__'))

    def test_validate_rapid_test_not_done(self):
        """test if the rapid test is not done"""
        self.data.update(
            rapid_test_done=NO,
            result_date=None,
            result=None)
        rapid_form = RapidTestResultForm(data=self.data)
        rapid_form.is_valid()
        self.assertFalse(rapid_form.is_valid())

    def test_rapid_test_result_present_no_rapid_test_done(self):
        """Test if the results are present and there is no rapid test performed"""
        self.data.update(
            rapid_test_done=NO,
            result_date=None,
            result=NEG)
        rapid_form = RapidTestResultForm(data=self.data)
        errors = ''.join(rapid_form.errors.get('__all__'))
        self.assertIn('If a rapid test was not processed, please do not provide the result. '
                      'Got {}.'.format(self.data['result']), errors)
