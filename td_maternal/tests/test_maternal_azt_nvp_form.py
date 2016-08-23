from tshilo_dikotla.choices import AZT_NVP
from .base_test_case import BaseTestCase


class TestMaternalAztNvp(BaseTestCase):

    def setUp(self):
        super(TestMaternalAztNvp, self).setUp()
        self.data = {'randomized': dict(AZT_NVP).get('AZT'),
                     'azt_nvp': dict(AZT_NVP).get('NVP'), }

    def test_validate_randomization_done(self):
        """Test if the chosen prophylaxis regiment match the randomized regiment"""
        self.data['randomized'] = dict(AZT_NVP).get('NVP')
        self.data['azt_nvp'] = dict(AZT_NVP).get('NVP')
        self.assertEqual(self.data['azt_nvp'], self.data['randomized'])
