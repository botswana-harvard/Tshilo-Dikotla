from edc_constants.constants import YES, NO

from ..forms import MaternalEligibilityForm
from .base_test_case import BaseTestCase


class TestMaternalEligibilityForm(BaseTestCase):

    data = {}

    def Setup(self):
        super(TestMaternalEligibilityForm, self).setUp()
#         self.data = {}

    def test_both_pregrant_and_delivered(self):
        self.data['currently_pregnant'] = YES
        self.data['recently_delivered'] = YES
        form = MaternalEligibilityForm(data=self.data)
        self.assertIn(
            'Participant CANNOT BE BOTH: pregnant & just delivered. Please Correct.',
            form.errors.get('__all__'))

    def test_not_pregrant_not_delivered(self):
        self.data['currently_pregnant'] = NO
        self.data['recently_delivered'] = NO
        form = MaternalEligibilityForm(data=self.data)
        self.assertIn(
            'A mother is either pregnant or she may have just delivered. Please Correct.',
            form.errors.get('__all__'))

    def test_delivered_and_no_hours(self):
        self.data['currently_pregnant'] = NO
        self.data['recently_delivered'] = YES
        form = MaternalEligibilityForm(data=self.data)
        self.assertIn(
            'The mother reports to have recently delivered. Enter No. hours since delivery.',
            form.errors.get('__all__'))

    def test_not_delivered_and_hours(self):
        self.data['currently_pregnant'] = YES
        self.data['recently_delivered'] = NO
        self.data['hours_delivered'] = 12
        form = MaternalEligibilityForm(data=self.data)
        self.assertIn(
            'The mother reports to still be pregnant. Hours since delivery must be blank.',
            form.errors.get('__all__'))
