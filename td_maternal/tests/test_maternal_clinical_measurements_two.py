from dateutil.relativedelta import relativedelta
from django.utils import timezone
from model_mommy import mommy

from edc_constants.constants import UNKNOWN, YES, NEG, NOT_APPLICABLE, NO, POS
from td.models import Appointment

from td_maternal.forms import MaternalClinicalMeasurementsTwoForm

from .base_test_case import BaseTestCase
from edc_visit_tracking.constants import SCHEDULED

from ..mommy_recipes import fake


class TestMaternalClinicalMeasurementsTwo(BaseTestCase):

    def setUp(self):
        super(TestMaternalClinicalMeasurementsTwo, self).setUp()
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject
        self.antenatal_visit_1 = None

        self.options = {
            'weight_kg': 76,
            'systolic_bp': 120,
            'diastolic_bp': 100}

    def test_diastolic_not_higher_than_systolic(self):
        """Test whether the Systolic Blood Pressure is not lower than the Diastolic Pressure"""

        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        self.options['matenal_visit'] = self.antenatal_visit_1
        self.options['systolic_bp'] = 100
        self.options['diastolic_bp'] = 120
        form = MaternalClinicalMeasurementsTwoForm(data=self.options)
        self.assertIn(
            'Systolic blood pressure cannot be lower than the diastolic blood pressure.'
            ' Please correct.', form.errors.get('__all__'))

    def test_systolic_not_blank(self):
        """Test if the Systolic blood pressure field is not empty"""

        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        self.options['matenal_visit'] = self.antenatal_visit_1
        self.options['systolic_bp'] = None
        form = MaternalClinicalMeasurementsTwoForm(data=self.options)
        self.assertIn('Systolic Blood Pressure field cannot be blank. Please correct', form.errors.get('__all__'))

    def test_diastolic_not_blank(self):
        """Test if the Diastolic pressure field is blank"""

        self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
        self.options['matenal_visit'] = self.antenatal_visit_1
        self.options['diastolic_bp'] = None
        form = MaternalClinicalMeasurementsTwoForm(data=self.options)
        self.assertIn('Diastolic Blood Pressure field cannot be blank. Please correct', form.errors.get('__all__'))

    def create_mother(self, antenatal_enrollment_options):
        self.antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment',
            **antenatal_enrollment_options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason=SCHEDULED)
        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)
        self.antenatal_enrollment_two = mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        self.maternal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit',
            appointment=self.appointment,
            reason=SCHEDULED)

    def hiv_pos_mother_options(self):
        options = {'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': fake.twenty_five_weeks_ago}
        return options

    def hiv_neg_mother_options(self):
        options = {'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': fake.four_weeks_ago,
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_result': NEG,
                   'last_period_date': fake.thirty_four_weeks_ago}
        return options
