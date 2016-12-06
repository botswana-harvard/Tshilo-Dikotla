from dateutil.relativedelta import relativedelta
from django.test import TestCase
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_code_lists.models import WcsDxAdult
from edc_constants.constants import (YES, NEG, NOT_APPLICABLE, NO)

from td.models import Appointment
from td_list.models import MaternalDiagnoses, MaternalHospitalization
from td_maternal.forms import MaternalPostPartumFuForm

from .mixins import AntenatalVisitsMotherMixin, PosMotherMixin, DeliverMotherMixin


class TestMaternalPostPartumFu(AntenatalVisitsMotherMixin, DeliverMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalPostPartumFu, self).setUp()

        self.diagnoses = MaternalDiagnoses.objects.create(
            hostname_created="django", name="Gestational Hypertension",
            short_name="Gestational Hypertension", created=get_utcnow(),
            user_modified="", modified=get_utcnow(),
            hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None, revision=None)

        self.diagnoses_na = MaternalDiagnoses.objects.create(
            hostname_created="django", name="N/A",
            short_name="N/A", created=get_utcnow(),
            user_modified="", modified=get_utcnow(),
            hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None,
            revision=":develop:")

        self.who_dx = WcsDxAdult.objects.create(
            hostname_created="cabel", code="CS4003", short_name="Recurrent severe bacterial pneumo",
            created=get_utcnow(), user_modified="", modified=get_utcnow(),
            hostname_modified="cabel",
            long_name="Recurrent severe bacterial pneumonia", user_created="abelc",
            list_ref="WHO CLINICAL STAGING OF HIV INFECTION 2006", revision=None)

        self.who_dx_na = WcsDxAdult.objects.create(
            hostname_created="cabel", code="cs9999999", short_name="N/A",
            created=get_utcnow(), user_modified="", modified=get_utcnow(),
            hostname_modified="cabel", long_name="N/A",
            user_created="abelc", list_ref="", revision=None)

        self.hospitalization_reason = MaternalHospitalization.objects.create(
            name="Pneumonia or other respiratory disease", short_name="Pneumonia or other respiratory disease",
            display_index=1, version="1.0", created=get_utcnow(), modified=get_utcnow(),
            user_created="", user_modified="", hostname_created="otse.bhp.org.bw",
            hostname_modified="otse.bhp.org.bw", revision=None)

        self.hospitalization_reason_na = MaternalHospitalization.objects.create(
            name="Not Applicable", short_name="N/A", display_index=2, version="1.0",
            created=get_utcnow(), modified=get_utcnow(), user_created="", user_modified="",
            hostname_created="otse.bhp.org.bw", hostname_modified="otse.bhp.org.bw", revision=None)

        self.add_maternal_visits('1000M', '1010M', '1020M', '2000M')

        maternal_visit = self.get_maternal_visit('2000M')
        self.options = {
            'maternal_visit': maternal_visit.id,
            'new_diagnoses': YES,
            'diagnoses': [self.diagnoses.id],
            'hospitalized': YES,
            'hospitalization_reason': [self.hospitalization_reason.id],
            'hospitalization_days': 1,
            'has_who_dx': YES,
            'who': [self.who_dx.id]}

    def test_diagnosis_list_none(self):
        """check if the diagnosis list is empty"""
        self.options['diagnoses'] = None
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Diagnosis field should not be left empty', errors)

    def test_new_diagnoses_no_diagnosis_list_no_not_applicable(self):
        """checks if the diagnosis list is given when the patient has no new diagnoses"""
        self.options['new_diagnoses'] = NO
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Participant has no new diagnoses, do not give a listing, rather give N/A', errors)

    def test_new_diagnoses_no_diagnosis_list_listed_has_not_applicable(self):
        """Checks if multiple options are selected with N/A as one of them"""
        self.options['new_diagnoses'] = NO
        self.options['diagnoses'] = [self.diagnoses.id, self.diagnoses_na.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Participant has no new diagnoses, do not give a listing, only give N/A', errors)

    def test_new_diagnoses_yes_diagnosis_list_has_not_applicable(self):
        """Checks if diagnoses listing is N/A even though mother has new diagnoses"""
        self.options['diagnoses'] = [self.diagnoses_na.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Participant has new diagnoses, list of diagnosis cannot be N/A', errors)

    def test_hospitalized_yes_hospitalization_reason_none(self):
        """check if the hospitalization reason is none"""
        self.options['hospitalization_reason'] = None
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question7: Patient was hospitalized, please give hospitalization_reason.', errors)

    def test_hospitalized_yes_hospitalization_reason_not_applicable(self):
        """check if hospitalization reason is N/A even though the mother was hospitalized"""
        self.options['hospitalization_reason'] = [self.hospitalization_reason_na.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question7: Participant was hospitalized, reasons cannot be N/A', errors)

    def test_hospitalization_yes_no_hospitalization_days(self):
        """Check that the number of hospitalization days has been given provided that the mother was hospitalized"""
        self.options['hospitalization_days'] = None
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question9: The mother was hospitalized, please give number of days hospitalized', errors)

    def test_hospitalized_no(self):
        """Check if the field for hospitalization reason is none"""
        self.options['hospitalized'] = NO
        self.options['hospitalization_reason'] = None
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question7: Participant was not hospitalized, reason should be N/A', errors)

    def test_hospitalized_no_hospitalization_reason_listed(self):
        """Check if the field for hospitalization reason is none"""
        self.options['hospitalized'] = NO
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question7: Participant was not hospitalized, reason should be N/A', errors)

    def test_hospitalized_no_hospitalization_reason_listed_with_not_applicable(self):
        """Check if the field for hospitalization reason is listed and has N/A as one of the options"""
        self.options['hospitalized'] = NO
        self.options['hospitalization_reason'] = [self.hospitalization_reason.id, self.hospitalization_reason_na.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question7: Participant was not hospitalized, reason should only be N/A', errors)

    def test_hospitalized_no_hospitalization_other_given(self):
        """Check if the field for hospitalization reason is listed and has N/A as one of the options"""
        self.options['hospitalized'] = NO
        self.options['hospitalization_reason'] = [self.hospitalization_reason_na.id]
        self.options['hospitalization_other'] = "Asthma"
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question8: Patient was not hospitalized, please do not give hospitalization reason.', errors)

    def test_hospitalized_no_hospitalization_date_given(self):
        """Check if the field for hospitalization reason is listed and has N/A as one of the options"""
        self.options['hospitalized'] = NO
        self.options['hospitalization_reason'] = [self.hospitalization_reason_na.id]
        self.options['hospitalization_other'] = None
        self.options['hospitalization_days'] = 5
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question9: Patient was not hospitalized, please do not give hospitalization days', errors)

    def test_mother_negative_who_diagnosis_yes(self):
        """checks whether question 10 for WHO Stage III/IV is N/A if the mother is negative"""
        self.maternal_eligibility_2 = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent_2 = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility_2, first_name='TATA',
            last_name='TATA', identity="111121112", confirm_identity="111121112")

        self.registered_subject_2 = self.maternal_consent_2.maternal_eligibility.registered_subject
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject_2))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='1020M')
        maternal_visit_1020M = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_1020M, result_date=get_utcnow(), result=NEG)
        mommy.make_recipe('td_maternal.maternallabdel', registered_subject=self.registered_subject_2)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='2000M')
        maternal_visit_2010M = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_2010M, result_date=get_utcnow(), result=NEG)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='2010M')
        self.maternal_visit_2000 = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.options['maternal_visit'] = self.maternal_visit_2000.id
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('The mother is Negative, question 10 for WHO Stage III/IV should be N/A', errors)

    def test_mother_negative_who_listing_none(self):
        """Checks if the field for who diagnosis listing is empty"""
        self.maternal_eligibility_2 = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent_2 = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility_2,
            first_name='TATA', last_name='TATA', identity="111121112", confirm_identity="111121112")

        self.registered_subject_2 = self.maternal_consent_2.maternal_eligibility.registered_subject
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject_2))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='1020M')
        maternal_visit_1020M = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_1020M, result_date=get_utcnow(), result=NEG)
        mommy.make_recipe('td_maternal.maternallabdel', registered_subject=self.registered_subject_2)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='2000M')
        maternal_visit_2010M = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_2010M, result_date=get_utcnow(), result=NEG)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='2010M')
        self.maternal_visit_2000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.options['maternal_visit'] = self.maternal_visit_2000.id
        self.options['has_who_dx'] = NOT_APPLICABLE
        self.options['who'] = None
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question11: Participant is HIV NEG, WHO Diagnosis field should be N/A', errors)

    def test_mother_negative_who_listing_not_not_applicable(self):
        """checks if who listing is N/A given that the mother is negative"""
        self.maternal_eligibility_2 = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent_2 = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility_2,
            first_name='TATA', last_name='TATA', identity="111121112", confirm_identity="111121112")

        self.registered_subject_2 = self.maternal_consent_2.maternal_eligibility.registered_subject
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject_2))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='1020M')
        maternal_visit_1020M = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_1020M, result_date=get_utcnow(), result=NEG)
        mommy.make_recipe('td_maternal.maternallabdel', registered_subject=self.registered_subject_2)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='2000M')
        maternal_visit_2010M = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_2010M, result_date=get_utcnow(), result=NEG)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='2010M')
        self.maternal_visit_2000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.options['maternal_visit'] = self.maternal_visit_2000.id
        self.options['has_who_dx'] = NOT_APPLICABLE
        self.options['who'] = [self.who_dx.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('The mother is Negative, question 11 for WHO Stage III/IV listing should be N/A', errors)

    def test_mother_negative_who_listed_not_applicable_there(self):
        """checks if who listing is only N/A if multiple options are selected given that the mother is negative"""
        self.maternal_eligibility_2 = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent_2 = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility_2,
            first_name='TATA', last_name='TATA', identity="111121112", confirm_identity="111121112")

        self.registered_subject_2 = self.maternal_consent_2.maternal_eligibility.registered_subject
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject_2))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='1020M')
        maternal_visit_1020M = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_1020M, result_date=get_utcnow(), result=NEG)
        mommy.make_recipe('td_maternal.maternallabdel', registered_subject=self.registered_subject_2)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='2000M')
        maternal_visit_2010M = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        mommy.make_recipe(
            'td_maternal.rapidtestresult', maternal_visit=maternal_visit_2010M, result_date=get_utcnow(), result=NEG)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject_2.subject_identifier, visit_code='2010M')
        self.maternal_visit_2000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.options['maternal_visit'] = self.maternal_visit_2000.id
        self.options['has_who_dx'] = NOT_APPLICABLE
        self.options['who'] = [self.who_dx.id, self.who_dx_na.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'The mother is Negative, question 11 for WHO Stage III/IV listing should only be N/A', errors)

    def test_mother_positive_who_diagnosis_not_applicable(self):
        """checks if question 10 for WHO Stage III/IV is not N/A given that the mother is positive"""
        self.options['has_who_dx'] = NOT_APPLICABLE
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('The mother is positive, question 10 for WHO Stage III/IV should not be N/A', errors)

    def test_mother_positive_who_listing_none(self):
        """Checks if who listing is none"""
        self.options['who'] = None
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question11: WHO Diagnosis field should not be left empty', errors)

    def test_mother_positive_who_diagnoses_yes_who_listing_not_applicable(self):
        """checks if who listing is not N/A provided question 10 is yes"""
        self.options['who'] = [self.who_dx_na.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question 10 is indicated as YES, who listing cannot be N/A', errors)

    def test_mother_positive_who_diagnoses_no_who_listed_not_applicable_not_there(self):
        """checks if who listing is N/A given that question 10 is No"""
        self.options['has_who_dx'] = NO
        self.options['who'] = [self.who_dx.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question 10 is indicated as NO, who listing should be N/A', errors)

    def test_mother_positive_who_diagnoses_no_who_listed_not_applicable_there(self):
        """checks if who listing is only N/A"""
        self.options['has_who_dx'] = NO
        self.options['who'] = [self.who_dx.id, self.who_dx_na.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question 10 is indicated as NO, who listing should only be N/A', errors)
