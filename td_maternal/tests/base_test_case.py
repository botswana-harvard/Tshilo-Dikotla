from django.test.testcases import TestCase

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import date
from model_mommy import mommy

from edc_constants.constants import (YES, NEG, NOT_APPLICABLE, POS, NO)
from td.models import Appointment

from ..mommy_recipes import fake


class BaseTestCase(TestCase):

    def setUp(self):
        self.study_site = '40'
        self.options = {}

        # Create a positive mother

        self.maternal_eligibility_pos = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent_pos = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility_reference=self.maternal_eligibility_pos.reference_pk)
        self.options = {'subject_identifier': self.maternal_consent_pos.subject_identifier}
        self.antenatal_enrollment_pos = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **self.options)
        self.appointment_1000_pos = Appointment.objects.get(
            subject_identifier=self.options.get('subject_identifier'), visit_code='1000M')
        self.maternal_visit_1000_pos = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment_1000_pos, reason='scheduled')
        self.maternal_ultrasound_pos = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)
        self.antenatal_enrollment_two_pos = mommy.make_recipe('td_maternal.antenatal_enrollment_common_two', **self.options)
        self.appointment_1010M_pos = Appointment.objects.get(
            subject_identifier=self.options.get('subject_identifier'), visit_code='1010M')
        self.antenatal_visit_1_pos = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment_1000_pos, reason='scheduled')

        # Create a negative mother

        self.maternal_eligibility_neg = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent_neg = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility_reference=self.maternal_eligibility_neg.reference_pk)
        self.options = {'subject_identifier': self.maternal_consent_neg.subject_identifier}
        self.antenatal_enrollment_neg = mommy.make_recipe('td_maternal.antenatalenrollment_neg', **self.options)
        self.appointment_1000_neg = Appointment.objects.get(
            subject_identifier=self.options.get('subject_identifier'), visit_code='1000M')
        self.maternal_visit_1000_neg = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment_1000_neg, reason='scheduled')

        self.maternal_ultrasound_neg = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000_neg, number_of_gestations=1)

        self.antenatal_enrollment_two_neg = mommy.make_recipe(
            'td_maternal.antenatal_enrollment_common_two', subject_identifier=self.options.get('subject_identifier'))
        self.appointment_1010_neg = Appointment.objects.get(
            subject_identifier=self.options.get('subject_identifier'), visit_code='1010M')
        self.antenatal_visit_1_neg = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment_1010_neg, reason='scheduled')
