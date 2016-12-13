from django.test import TestCase

from model_mommy import mommy

from edc_constants.constants import POS, YES, NO
from edc_visit_tracking.constants import SCHEDULED

from td.models import Appointment
from td_infant.forms import InfantFuDxItemsForm

from .test_mixins import InfantMixin


class TestInfantFuDxItemsForm(InfantMixin, TestCase):

    def setUp(self):
        super(TestInfantFuDxItemsForm, self).setUp()
        self.make_infant_birth(maternal_status=POS)
        infant_appointment_2000 = Appointment.objects.get(subject_identifier=self.infant_identifier, visit_code='2000')
        mommy.make_recipe(
            'td_infant.infantvisit',
            appointment=infant_appointment_2000,
            report_datetime=infant_appointment_2000.appt_datetime,
            reason=SCHEDULED)

        infant_appointment_2010 = Appointment.objects.get(subject_identifier=self.infant_identifier, visit_code='2010')
        mommy.make_recipe(
            'td_infant.infantvisit',
            appointment=infant_appointment_2010,
            report_datetime=infant_appointment_2010.appt_datetime,
            reason=SCHEDULED)
        self.make_infant_birth_arv(infant_visit=self.get_infant_visit('2000'))

        self.infantfu = mommy.make_recipe(
            'td_infant.infantfu',
            infant_visit=self.get_infant_visit('2010'),
            was_hospitalized=YES)

        self.infant_fu_dx = mommy.make_recipe(
            'td_infant.infantfudx',
            infant_visit=self.get_infant_visit('2010'))

        self.options = {'infant_vist': self.get_infant_visit('2010'),
                        'infant_fu_dx': self.infant_fu_dx.id,
                        'fu_dx': 'Appendicitis',
                        'fu_dx_specify': None,
                        'health_facility': YES,
                        'was_hospitalized': YES,
                        }

    def test_validate_seen_at_health_facility(self):
        """Test validate if the participant was hospitalized and seen at a health facility"""
        self.options['was_hospitalized'] = YES
        self.options['health_facility'] = NO
        infant_fu_dx_items = InfantFuDxItemsForm(data=self.options)
        self.assertIn(
            'You indicated that participant was hospitalized, therefore the participant '
            'was seen at a health facility. Please correct.',
            infant_fu_dx_items.errors.get('__all__'))

    def test_validate_reported_hospitalization(self):
        """Test validate if Question6 on Infant Follow Up form is answered YES"""
        self.infantfu.was_hospitalized = NO
        self.infantfu.save()
        self.options.update(infant_fu_dx=self.infant_fu_dx.id)
        infant_fu_dx_items = InfantFuDxItemsForm(data=self.options)
        self.assertIn('Question6 in Infant Follow Up is not answered YES, you cannot fill this form.',
                      infant_fu_dx_items.errors.get('__all__'))

    def test_validate_other_serious_grade3or4_infection_specification(self):
        """Test if diagnosis specification for infections is provided"""
        self.options['fu_dx'] = 'Other serious (grade 3 or 4)infection(not listed above),specify'
        self.options['fu_dx_specify'] = None
        infant_fu_dx = InfantFuDxItemsForm(data=self.options)
        self.assertIn('You mentioned there is other serious (grade 3 or 4) infection, Please specify',
                      infant_fu_dx.errors.get('__all__'))

    def test_other_serious_grade3or4_non_infectious_specification(self):
        """Test if diagnosis specification for non-infectious is provided"""
        self.options['fu_dx'] = 'Other serious (grade 3 or 4) non-infectious(not listed above),specify'
        self.options['fu_dx_specify'] = None
        infant_fu_dx = InfantFuDxItemsForm(data=self.options)
        self.assertIn('You mentioned there is other serious (grade 3 or 4) non-infectious, Please specify',
                      infant_fu_dx.errors.get('__all__'))

    def test_other_abnormallaboratory_tests_specification(self):
        """Test if test and result of other abnormal laboratory is provided"""
        self.options['fu_dx'] = 'Other abnormallaboratory tests(other than tests listed above ''or tests done as part of this study), specify test and result'
        self.options['fu_dx_specify'] = None
        infant_fu_dx = InfantFuDxItemsForm(data=self.options)
        self.assertIn('You mentioned there is abnormallaboratory tests, Please specify',
                      infant_fu_dx.errors.get('__all__'))

    def test_validate_new_congenital_abnormality_not_previously_identified_specification(self):
        """Test if new congenital abnormality not previously identified is specified'"""
        self.options['fu_dx'] = 'New congenital abnormality not previously identified?,specify'
        self.options['fu_dx_specify'] = None
        infant_fu_dx = InfantFuDxItemsForm(data=self.options)
        self.assertIn('You mentioned there is new congenital abnormality not previously identified , Please specify',
                      infant_fu_dx.errors.get('__all__'))
