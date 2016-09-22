from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from td_registration.models import RegisteredSubject
from edc_identifier.models import SubjectIdentifier
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, POS, YES, NO, NOT_APPLICABLE, UNKNOWN

from td_appointment.models import Appointment

from td_maternal.models import MaternalVisit

from td_infant.forms import InfantFeedingForm

from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabourDelFactory,
                                         MaternalVisitFactory)

from .factories import (InfantBirthFactory, InfantVisitFactory, InfantArvProphFactory, InfantBirthArvFactory,
                        InfantFuImmunizationsFactory)

from td_maternal.tests import BaseTestCase


class TestInfantFeedingForm(BaseTestCase):

    def setUp(self):
        super(TestInfantFeedingForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.infant_birth_arv = InfantBirthArvFactory(infant_visit=self.infant_visit, azt_discharge_supply=YES)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)

        self.options = {
            'infant_visit': self.infant_visit.id,
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
