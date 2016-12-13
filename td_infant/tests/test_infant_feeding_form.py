from datetime import date
from django.test import TestCase
from model_mommy import mommy

from edc_constants.constants import POS, YES, NO, NOT_APPLICABLE
from edc_visit_tracking.constants import SCHEDULED

from td.models import Appointment

from td_infant.forms import InfantFeedingForm

from .test_mixins import InfantMixin


class TestInfantFeedingForm(InfantMixin, TestCase):

    def setUp(self):
        super(TestInfantFeedingForm, self).setUp()

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

        self.options = {
            'infant_visit': self.get_infant_visit('2010').id,
            'other_feeding': YES,
            'formula_intro_occur': YES,
            'formula_intro_date': date.today(),
            'took_formula': YES,
            'is_first_formula': YES,
            'date_first_formula': date.today(),
            'est_date_first_formula': YES,
            'water': YES,
            'juice': YES,
            'cow_milk': YES,
            'cow_milk_yes': 'boiled',
            'other_milk': NO,
            'other_milk_animal': None,
            'milk_boiled': NOT_APPLICABLE,
            'fruits_veg': NO,
            'cereal_porridge': NO,
            'solid_liquid': YES,
            'rehydration_salts': NO,
            'water_used': 'Water direct from source',
            'water_used_other': None,
            'ever_breastfeed': YES,
            'complete_weaning': NOT_APPLICABLE,
            'weaned_completely': NO,
            'most_recent_bm': None,
            'times_breastfed': '<1 per week',
            'comments': ''}

    def test_child_received_other_feeding_date_no_date(self):
        """Test that if the child received other feeding, the date the food was introduced is given"""
        self.options['formula_intro_date'] = None
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question3: If received formula milk | foods | liquids since last"
                      " attended visit. Please provide intro date", forms.errors.get('__all__'))

    def test_child_not_received_other_feeding_date_given(self):
        """Test that if the child did not receive other feeding, the date the food was introduced is not given"""
        self.options['formula_intro_occur'] = NO
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("You mentioned no formula milk | foods | liquids received"
                      " since last visit in question 3. DO NOT PROVIDE DATE", forms.errors.get('__all__'))

    def test_infant_formula_feeding_YES(self):
        """"Test if the child took formula, the field for whether this is the first reporting in not N/A"""
        self.options['is_first_formula'] = None
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question7: Infant took formula, is this the first reporting of infant formula use? Please"
                      " provide YES or NO", forms.errors.get('__all__'))

    def test_infant_formula_feeding_not_yes(self):
        """Test if the child did not take formula, the field for whether this is the first reporting is N/A not YES"""
        self.options['took_formula'] = NO
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question7: You mentioned that infant did not take formula, PLEASE DO NOT PROVIDE FIRST FORMULA"
                      " USE INFO", forms.errors.get('__all__'))

    def test_infant_formula_feeding_not_yes_date_provided(self):
        """Test if the child did not take formula, the field for whether this is the first reporting is N/A not None"""
        self.options['took_formula'] = NO
        self.options['is_first_formula'] = None
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question8: You mentioned that infant did not take formula, PLEASE DO NOT PROVIDE DATE OF"
                      " FIRST FORMULA USE", forms.errors.get('__all__'))

    def test_infant_formula_feeding_not_yes_est_date_provided(self):
        """Test if the child did not take formula, the date of estimated first formula use is not provided"""
        self.options['took_formula'] = NO
        self.options['is_first_formula'] = None
        self.options['date_first_formula'] = None
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question9: You mentioned that infant did not take formula, PLEASE DO NOT PROVIDE ESTIMATED DATE"
                      " OF FIRST FORMULA USE", forms.errors.get('__all__'))

    def test_is_first_formula_yes_no_date(self):
        """Test that if this is the first reporting of infant formula, the date should be provided"""
        self.options['date_first_formula'] = None
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("If this is a first reporting of infant formula"
                      " please provide date and if date is estimated", forms.errors.get('__all__'))

    def test_is_first_formula_yes_date_estimated_field_none(self):
        """Test that if this is the first reporting of infant formula, whether the date is estimated should be indicated"""
        self.options['date_first_formula'] = None
        self.options['est_date_first_formula'] = None
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("If this is a first reporting of infant formula"
                      " please provide date and if date is estimated", forms.errors.get('__all__'))

    def test_is_first_formula_no_date_provided(self):
        """Test that if this is not the first reporting of infant formula, the date should not be provided"""
        self.options['is_first_formula'] = NO
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question8: You mentioned that is not the first reporting of infant formula"
                      " PLEASE DO NOT PROVIDE DATE", forms.errors.get('__all__'))

    def test_is_first_formula_no_date_estimated_given(self):
        """Test that if this is not the first reporting of infant formula, whether the date is estimated should not
           be indicated"""
        self.options['is_first_formula'] = NO
        self.options['date_first_formula'] = None
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question9: You mentioned that is not the first reporting of infant formula"
                      " PLEASE DO NOT PROVIDE EST DATE", forms.errors.get('__all__'))

    def test_took_cow_milk_yes(self):
        """test that if the infant received cow milk, the field question13 should not be N/A"""
        self.options['cow_milk_yes'] = NOT_APPLICABLE
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question13: If infant took cows milk. Answer CANNOT be Not Applicable",
                      forms.errors.get('__all__'))

    def test_took_cow_milk__not_yes(self):
        """test that if the infant did not receive cow milk, the field question13 should be N/A"""
        self.options['cow_milk'] = NO
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question13: Infant did not take cows milk. Answer is NOT APPLICABLE",
                      forms.errors.get('__all__'))

    def test_took_milk_other_yes_animal_not_specified(self):
        """Test that if the infant took milk from another animal, that animal is specified"""
        self.options['other_milk'] = YES
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question15: The infant took milk from another animal, please specify which?",
                      forms.errors.get('__all__'))

    def test_took_milk__yes_milk_boiled_not_applicable(self):
        """Test that if the infant took milk from another animal, the answer to Question16 is not N/A"""
        self.options['other_milk'] = YES
        self.options['other_milk_animal'] = 'Goat'
        self.options['milk_boiled'] = NOT_APPLICABLE
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question16:The infant took milk from another animal, answer"
                      " cannot be N/A", forms.errors.get('__all__'))

    def test_took_milk_other_not_yes_animal_specified(self):
        """Test that if the infant did not take milk from another animal, that animal is not specified"""
        self.options['other_milk_animal'] = 'Goat'
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question15: The infant did not take milk from any other animal, please"
                      " do not provide the name of the animal", forms.errors.get('__all__'))

    def test_took_milk_other_not_yes_boiled_not_not_applicable(self):
        """Test that if the infant did not take milk from another animal, the answer to question 16 is N/A"""
        self.options['milk_boiled'] = YES
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question16: The infant did not take milk from any other animal, the"
                      " answer for whether the milk was boiled should be N/A", forms.errors.get('__all__'))

    def test_child_breastfed_complete_weaning_not_not_applicable(self):
        """Test that if the infant has been breast fed since the last visit, the answer to question24 is N/A"""
        self.options['complete_weaning'] = NO
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question24: The infant has been breastfed since the last visit, The answer"
                      " answer should be N/A", forms.errors.get('__all__'))

    def test_child_not_breastfed_complete_weaning_not_applicable(self):
        """Test that if the child has not been breast fed since the last visit, the answer to question24 should not be
        NA"""
        self.options['ever_breastfeed'] = NO
        self.options['complete_weaning'] = NOT_APPLICABLE
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("Question24: The infant has not been breastfed since the last visit, "
                      "The answer should not be N/A", forms.errors.get('__all__'))

    def test_formula_intro_occur_yes_no_foods_indicated(self):
        self.options['juice'] = NO
        self.options['cow_milk'] = NO
        self.options['cow_milk_yes'] = NOT_APPLICABLE
        self.options['other_milk'] = NO
        self.options['fruits_veg'] = NO
        self.options['cereal_porridge'] = NO
        self.options['solid_liquid'] = NO
        forms = InfantFeedingForm(data=self.options)
        self.assertIn("You should answer YES on either one of the questions about the juice, cow_milk, other milk, "
                      "fruits_veg, cereal_porridge or solid_liquid", forms.errors.get('__all__'))
