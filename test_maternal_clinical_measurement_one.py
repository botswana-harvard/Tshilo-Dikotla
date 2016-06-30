from .base_test_case import BaseTestCase

from .factories import (MaternalEligibilityFactory, MaternalConsentFactory)
from tshilo_dikotla.apps.td_maternal.forms import MaternalClinicalMeasurementsOneForm

class TestMaternalClinicalMeasurementOne(BaseTestCase):

    def setUp(self):
        super(TestMaternalClinicalMeasurementOne, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.data ={
        'systolic_bp' : 75,          
        'diastolic_bp': 120           
                    }
    def test_systolic_bp_lower_than_diastolic_bp(self):
        self.data['systolic_bp'] = 40
        self.data['diastolic_bp'] = 80
        form = MaternalClinicalMeasurementsOneForm(data=self.data)
        self.assertIn('Systolic blood pressure cannot be lower than the diastolic blood pressure.'
                ' Please correct.',form.errors.get('__all__') )
