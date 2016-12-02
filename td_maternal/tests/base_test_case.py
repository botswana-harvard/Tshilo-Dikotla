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
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility_reference=self.maternal_eligibility.reference_pk)
        self.options = {'subject_identifier': self.maternal_consent.subject_identifier}

    def eligible_hiv_pos_mother(self, options):
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_pos', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('subject_identifier'), visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)

        self.antenatal_enrollment_two = mommy.make_recipe('td_maternal.antenatal_enrollment_common_two', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('subject_identifier'), visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

    def eligible_neg_pos_mother(self, options):
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment_neg', **options)
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('subject_identifier'), visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)

        self.antenatal_enrollment_two = mommy.make_recipe(
            'td_maternal.antenatal_enrollment_common_two', subject_identifier=options.get('subject_identifier'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('subject_identifier'), visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
