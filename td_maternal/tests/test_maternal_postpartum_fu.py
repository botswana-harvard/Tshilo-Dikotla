from django.test import TestCase, tag

from edc_base.test_mixins import LoadListDataMixin
from edc_constants.constants import YES, NOT_APPLICABLE, NO

from td_list.models import AdultDiagnosis, MaternalHospitalization, WhoAdultDiagnosis

from ..forms import MaternalPostPartumFuForm

from .test_mixins import MotherMixin


class DxMixin(LoadListDataMixin):
    def setUp(self):
        super(DxMixin, self).setUp()
        self.load_list_data('td_list.adultdiagnosis')
        self.load_list_data('td_list.whoadultdiagnosis')
        self.load_list_data('td_list.maternalhospitalization')
        self.diagnoses = AdultDiagnosis.objects.get(name="Gestational Hypertension")
        self.diagnoses_na = AdultDiagnosis.objects.get(name=NOT_APPLICABLE)
        self.who_dx = WhoAdultDiagnosis.objects.get(name='Recurrent severe bacterial pneumo')
        self.who_dx_na = WhoAdultDiagnosis.objects.get(name=NOT_APPLICABLE)
        self.hospitalization_reason = MaternalHospitalization.objects.get(
            name="Pneumonia or other respiratory disease")
        self.hospitalization_reason_na = MaternalHospitalization.objects.get(name=NOT_APPLICABLE)
        self.options = {
            'new_diagnoses': YES,
            'diagnoses': [str(self.diagnoses.id)],
            'hospitalized': YES,
            'hospitalization_reason': [str(self.hospitalization_reason.id)],
            'hospitalization_days': 1,
            'has_who_dx': YES,
            'who': [self.who_dx.id]}


@tag('review')
class TestMaternalPostPartumFuPos(DxMixin, MotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalPostPartumFuPos, self).setUp()
        self.make_positive_mother()
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        self.make_delivery()
        self.add_maternal_visits('2000M', '2010M')
        maternal_visit = self.add_maternal_visit('2010M')
        self.options.update(maternal_visit=maternal_visit.id)

    def test_diagnosis_list_none(self):
        """Assert diagnosis may not be empty"""
        self.options.update(diagnoses=None)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Diagnosis field should not be left empty', errors)

    def test_new_diagnoses_no_diagnosis_list_no_not_applicable(self):
        """Assert diagnosis list is blank if no new diagnoses"""
        self.options.update(new_diagnoses=NO)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Participant has no new diagnoses, do not give a listing, rather give N/A', errors)

    def test_new_diagnoses_no_diagnosis_list_listed_has_not_applicable(self):
        """Assert N/A cannot be amongst multiple options selected."""
        self.options.update(
            new_diagnoses=NO,
            diagnoses=[str(self.diagnoses.id), str(self.diagnoses_na.id)])
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Participant has no new diagnoses, do not give a listing, only give N/A', errors)

    def test_new_diagnoses_yes_diagnosis_list_has_not_applicable(self):
        """Assert N/A is invalid if new diagnoses."""
        self.options.update(diagnoses=[str(self.diagnoses_na.id)])
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Participant has new diagnoses, list of diagnosis cannot be N/A', errors)

    def test_hospitalized_yes_hospitalization_reason_none(self):
        """check if the hospitalization reason is none"""
        self.options.update(hospitalization_reason=None)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question7: Patient was hospitalized, please give hospitalization_reason.', errors)

    def test_hospitalized_yes_hospitalization_reason_not_applicable(self):
        """check if hospitalization reason is N/A even though the mother was hospitalized"""
        self.options.update(hospitalization_reason=[str(self.hospitalization_reason_na.id)])
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question7: Participant was hospitalized, reasons cannot be N/A', errors)

    def test_hospitalization_yes_no_hospitalization_days(self):
        """Check that the number of hospitalization days has been given provided that the mother was hospitalized"""
        self.options.update(hospitalization_days=None)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question9: The mother was hospitalized, please give number of days hospitalized', errors)

    def test_hospitalized_no(self):
        """Check if the field for hospitalization reason is none"""
        self.options.update(
            hospitalized=NO,
            hospitalization_reason=None)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question7: Participant was not hospitalized, reason should be N/A', errors)

    def test_hospitalized_no_hospitalization_reason_listed(self):
        """Check if the field for hospitalization reason is none"""
        self.options.update(hospitalized=NO)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question7: Participant was not hospitalized, reason should be N/A', errors)

    def test_hospitalized_no_hospitalization_reason_listed_with_not_applicable(self):
        """Check if the field for hospitalization reason is listed and has N/A as one of the options"""
        self.options.update(
            hospitalized=NO,
            hospitalization_reason=[str(self.hospitalization_reason.id), str(self.hospitalization_reason_na.id)])
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question7: Participant was not hospitalized, reason should only be N/A', errors)

    def test_hospitalized_no_hospitalization_other_given(self):
        """Check if the field for hospitalization reason is listed and has N/A as one of the options"""
        self.options.update(
            hospitalized=NO,
            hospitalization_reason=[str(self.hospitalization_reason_na.id)],
            hospitalization_other="Asthma")
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question8: Patient was not hospitalized, please do not give hospitalization reason.', errors)

    def test_hospitalized_no_hospitalization_date_given(self):
        """Check if the field for hospitalization reason is listed and has N/A as one of the options"""
        self.options.update(
            hospitalized=NO,
            hospitalization_reason=[str(self.hospitalization_reason_na.id)],
            hospitalization_other=None,
            hospitalization_days=5)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question9: Patient was not hospitalized, please do not give hospitalization days', errors)

    def test_mother_positive_who_diagnosis_not_applicable(self):
        """checks if question 10 for WHO Stage III/IV is not N/A given that the mother is positive"""
        self.options.update(has_who_dx=NOT_APPLICABLE)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('The mother is positive, question 10 for WHO Stage III/IV should not be N/A', errors)

    def test_mother_positive_who_listing_none(self):
        """Checks if who listing is none"""
        self.options.update(who=None)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question11: WHO Diagnosis field should not be left empty', errors)

    def test_mother_positive_who_diagnoses_yes_who_listing_not_applicable(self):
        """checks if who listing is not N/A provided question 10 is yes"""
        self.options.update(who=[str(self.who_dx_na.id)])
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question 10 is indicated as YES, WHO listing cannot be N/A', errors)

    def test_mother_positive_who_diagnoses_no_who_listed_not_applicable_not_there(self):
        """checks if who listing is N/A given that question 10 is No"""
        self.options.update(
            has_who_dx=NO,
            who=[str(self.who_dx.id)])
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question 10 is indicated as NO, who listing should be N/A', errors)

    def test_mother_positive_who_diagnoses_no_who_listed_not_applicable_there(self):
        """checks if who listing is only N/A"""
        self.options.update(
            has_who_dx=NO,
            who=[str(self.who_dx.id), str(self.who_dx_na.id)])
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question 10 is indicated as NO, who listing should only be N/A', errors)


class TestMaternalPostPartumFuNegMother(DxMixin, MotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalPostPartumFuNegMother, self).setUp()
        self.make_negative_mother()
        self.add_maternal_visits('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        self.make_delivery()
        self.add_maternal_visits('2000M', '2010M')
        maternal_visit = self.add_maternal_visit('2010M')
        self.options.update(maternal_visit=maternal_visit.id)

    def test_mother_negative_who_diagnosis_yes(self):
        """Assert question 10 for WHO Stage III/IV is N/A if the mother is negative"""
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('The mother is Negative, question 10 for WHO Stage III/IV should be N/A', errors)

    def test_mother_negative_who_listing_none(self):
        """Checks if the field for who diagnosis listing is empty"""
        self.options.update(
            has_who_dx=NOT_APPLICABLE,
            who=None)
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Question11: Participant is HIV NEG, WHO Diagnosis field should be N/A', errors)

    def test_mother_negative_who_listing_not_not_applicable(self):
        """checks if who listing is N/A given that the mother is negative"""
        self.options.update(
            has_who_dx=NOT_APPLICABLE,
            who=[str(self.who_dx.id)])
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('The mother is Negative, question 11 for WHO Stage III/IV listing should be N/A', errors)

    def test_mother_negative_who_listed_not_applicable_there(self):
        """checks if who listing is only N/A if multiple options are selected given that the mother is negative"""
        self.options.update(
            has_who_dx=NOT_APPLICABLE,
            who=[str(self.who_dx.id), str(self.who_dx_na.id)])
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'The mother is Negative, question 11 for WHO Stage III/IV listing should only be N/A', errors)
