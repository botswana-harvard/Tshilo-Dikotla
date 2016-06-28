from django.utils import timezone

from edc_constants.constants import YES, NO, POS, NEG, IND

from tshilo_dikotla.apps.td_maternal.tests.factories import MaternalEligibilityFactory
from tshilo_dikotla.apps.td_maternal.tests.factories import MaternalConsentFactory
from tshilo_dikotla.apps.td_maternal.forms import RapidTestResultForm

from .base_test_case import BaseTestCase

class TestRapidTestForm(BaseTestCase):

    def setUp(self):
        super(TestRapidTestForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.assertTrue(self.maternal_eligibility.is_eligible)
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.data = {
            'rapid_test_done': YES,
            'result_date': timezone.now(),
            'result': NEG,
            }
    def test_result_date_provided(self):
        """Test if result date of the rapid test is provided"""
        self.data['rapid_test_done'] = YES
        self.data['result_date'] = None
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn('If a rapid test was processed, what is the date'
        ' of the rapid test?', rapid_form.errors.get('__all__'))

    def test_rapid_test_results(self):
        """Test if the result of rapid test is provided"""
        self.data['rapid_test_done'] = YES
        self.data['result'] = None
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn('If a rapid test was processed, what is the test result?',
        rapid_form.errors.get('__all__'))

    def test_result_date_present_no_rapid_test_result(self):
        """Test if there is a date for test and there is no test"""
        self.data['rapid_test_done'] = NO
        self.data['result_date'] = timezone.now()
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn('If a rapid test was not processed, please do not provide the result date. ',
        rapid_form.errors.get('__all__'))
  
    def test_rapid_test_result_present_no_rapid_test_done(self):
        """Test if the results are present and there is no rapid test performed"""
        self.data['rapid_test_done'] = NO
        self.data['result_date'] = None
        self.data['result'] = NEG
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn('If a rapid test was not processed, please do not provide the result. ',
        rapid_form.errors.get('__all__'))
