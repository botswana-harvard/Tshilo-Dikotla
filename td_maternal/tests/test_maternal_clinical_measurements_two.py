from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_constants.constants import UNKNOWN, YES, NEG, NOT_APPLICABLE, SCHEDULED, NO, POS
from td_appointment.models import Appointment

from td_maternal.forms import MaternalClinicalMeasurementsTwoForm
from td_maternal.models import MaternalVisit

from .factories import (MaternalEligibilityFactory, MaternalConsentFactory, AntenatalEnrollmentFactory,
                        MaternalUltraSoundIniFactory, AntenatalVisitMembershipFactory, MaternalVisitFactory)
from .base_test_case import BaseTestCase


class TestMaternalClinicalMeasurementsTwo(BaseTestCase):

    def setUp(self):
        super(TestMaternalClinicalMeasurementsTwo, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
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

    def create_mother(self, status_options):
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**status_options)
        self.maternal_visit_1000 = MaternalVisit.objects.get(
            appointment__registered_subject=status_options.get('registered_subject'),
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit_1000,
                                                                number_of_gestations=1
                                                                )
        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=status_options.get('registered_subject'))
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=status_options.get('registered_subject'),
                                                visit_definition__code='1010M'))

    def hiv_pos_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        return options

    def hiv_neg_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_result': NEG,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}
        return options
