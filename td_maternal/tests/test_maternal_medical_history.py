from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_code_lists.models import WcsDxAdult
from edc_constants.constants import YES, NO, NOT_APPLICABLE, NEG

from td_list.models import ChronicConditions, MaternalMedications

from ..forms import MaternalMedicalHistoryForm
from ..maternal_hiv_status import MaternalHivStatus

from .mixins import NegMotherMixin, PosMotherMixin, AntenatalVisitsMotherMixin


class ChronicAndMedicationsMixin:

    def setUp(self):
        super(ChronicAndMedicationsMixin, self).setUp()

        self.chronic_cond = ChronicConditions.objects.create(
            hostname_created="django", name="Asthma", short_name="Asthma",
            created=get_utcnow(), user_modified="", modified=get_utcnow(), hostname_modified="",
            version=1.0, display_index=3, user_created="django", field_name=None, revision=":develop")

        self.chronic_cond_na = ChronicConditions.objects.create(
            hostname_created="django", name="Not Applicable", short_name="N/A",
            created=get_utcnow(), user_modified="", modified=get_utcnow(), hostname_modified="",
            version=1.0, display_index=3, user_created="django", field_name=None, revision=":develop")

        self.mother_medications = MaternalMedications.objects.create(
            hostname_created="django", name="Prenatal Vitamins", short_name="Prenatal Vitamins",
            created=get_utcnow(), user_modified="", modified=get_utcnow(), hostname_modified="django",
            version="1.0", display_index=5, user_created="django", field_name=None, revision=":develop")

        self.mother_medications_na = MaternalMedications.objects.create(
            hostname_created="django", name="Not Applicable", short_name="N/A",
            created=get_utcnow(), user_modified="", modified=get_utcnow(), hostname_modified="django",
            version="1.0", display_index=5, user_created="django", field_name=None, revision=":develop")

        self.who_dx = WcsDxAdult.objects.create(
            hostname_created="cabel", code="CS4003", short_name="Recurrent severe bacterial pneumo",
            created=get_utcnow(), user_modified=get_utcnow(), modified=get_utcnow(),
            hostname_modified="cabel", long_name="Recurrent severe bacterial pneumonia",
            user_created="abelc", list_ref="WHO CLINICAL STAGING OF HIV INFECTION 2006", revision=None)

        self.who_dx_na = WcsDxAdult.objects.create(
            hostname_created="cabel", code="cs9999999", short_name="N/A",
            created=get_utcnow(), user_modified="", modified=get_utcnow(),
            hostname_modified="cabel", long_name="N/A",
            user_created="abelc", list_ref="", revision=None)

        self.options = {
            'maternal_visit': self.get_maternal_visit('1000M').id,
            'chronic_since': YES,
            'who_diagnosis': YES,
            'who': [self.who_dx.id],
            'mother_chronic': [self.chronic_cond.id],
            'father_chronic': [self.chronic_cond.id],
            'mother_medications': [self.mother_medications.id],
            'sero_positive': YES,
            'date_hiv_diagnosis': get_utcnow().date(),
            'perinataly_infected': YES,
            'know_hiv_status': "Nobody",
            'lowest_cd4_known': YES,
            'cd4_count': 4,
            'cd4_date': get_utcnow().date(),
            'is_date_estimated': NO}


class TestMaternalMedicalHistoryPosMother(ChronicAndMedicationsMixin, AntenatalVisitsMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalMedicalHistoryPosMother, self).setUp()

    def test_mother_chronic_multiple_selection_not_applicable_there(self):
        """check that N/A is not selected with other options"""
        self.options.update(mother_chronic=[self.chronic_cond.id, self.chronic_cond_na.id])
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question6: You cannot select options that have N/A in them',
            form.errors.get('__all__'))

    def test_mother_chronic_none(self):
        """check that the field for mothers chronic conditions is not empty"""
        self.options.update(mother_chronic=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question6: The field for the chronic illnesses of the mother should not be left blank',
            form.errors.get('__all__'))

    def test_father_chronic_multiple_selection_not_applicable_there(self):
        """check that N/A is not selected with other options"""
        self.options.update(father_chronic=[self.chronic_cond.id, self.chronic_cond_na.id])
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question8: You cannot select options that have N/A in them',
            form.errors.get('__all__'))

    def test_father_chronic_none(self):
        """check that the field for father illnesses is not empty"""
        self.options.update(father_chronic=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question8: The field for the chronic illnesses of the father should not be left blank',
            form.errors.get('__all__'))

    def test_mother_medications_multiple_selection_not_applicable_there(self):
        """check that N/A is not selected with other options"""
        self.options.update(mother_medications=[self.mother_medications.id, self.mother_medications_na.id])
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question10: You cannot select options that have N/A in them',
            form.errors.get('__all__'))

    def test_mother_medications_none(self):
        """check that the field for mothers medications is not empty"""
        self.options.update(mother_medications=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question10: The field for the mothers medications should not be left blank',
            form.errors.get('__all__'))

    def test_mother_positive_chronic_since_yes_who_diagnosis_no(self):
        """The Mother is HIV Positive yet chronic_since is YES and who_diagnosis has been indicated as NO.
           should be YES"""
        self.options.update(chronic_since=YES, who_diagnosis=NO)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The mother is HIV positive, because Chronic_since is YES and Who Diagnosis should also be YES',
                      form.errors.get('__all__'))

    def test_positive_mother_chronic_since_no_who_diagnosis_not_applicable(self):
        """The Mother is HIV Positive yet chronic_since is NO and who_diagnosis has been indicated as NOT_APPLICABLE.
           should be YES"""
        self.options.update(chronic_since=NO, who_diagnosis=NOT_APPLICABLE)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The mother is HIV positive, because Chronic_since is NO and Who Diagnosis should also be NO',
                      form.errors.get('__all__'))

    def test_positive_mother_has_chronic_no_who_list(self):
        """Indicated that mother had chronic conditions and WHO stage 3 and 4 illness prior to current pregnancy
           but the WHO conditions not listed"""
        self.options.update(
            chronic_since=YES,
            who_diagnosis=YES,
            who=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question5: Mother has prior chronic illness, they should be listed', form.errors.get('__all__'))

    def test_positive_mother_has_chronic_who_list_has_not_applicable(self):
        """Indicated that mother had chronic conditions and WHO stage 3 and 4 illness prior to current pregnancy
           but the WHO conditions listed N/A"""
        self.options.update(
            chronic_since=YES,
            who_diagnosis=YES,
            who=[self.who_dx_na.id])
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question5: Participant indicated that they had WHO stage III and IV, list of diagnosis cannot be N/A',
            form.errors.get('__all__'))

    def test_positive_mother_no_chronic_who_listed_not_applicable_not_there(self):
        """The mother does not who stage III and IV, who listing shoul be N/A"""
        self.options.update(
            chronic_since=NO,
            who_diagnosis=NO,
            who=[self.who_dx.id])
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question5: The mother does not have prior who stage III and IV illnesses. Should provide N/A',
            form.errors.get('__all__'))

    def test_positive_mother_no_chronic_who_listed_not_applicable_there(self):
        """The mother does not who stage III and IV, who listing should be N/A"""
        self.options.update(
            chronic_since=NO,
            who_diagnosis=NO,
            who=[self.who_dx.id, self.who_dx_na.id])
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question5: The mother does not have prior who stage III and IV illnesses. Should only provide N/A',
            form.errors.get('__all__'))

    def test_mother_HIV_Sero_Positive_no(self):
        """the mother is HIV positive but it is indicated that she is not sero positive"""
        self.options.update(sero_positive=NO)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'The mother is HIV Positive, The field for whether she is sero positive should not be NO',
            form.errors.get('__all__'))

    def test_mother_HIV_Sero_Positive_diagnosis_date_blank(self):
        """the mother is HIV sero positive but the date of hiv diagnosis has not been supplied"""
        self.options.update(
            sero_positive=YES,
            date_hiv_diagnosis=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'The Mother is Sero-Positive, the approximate date of diagnosis should be supplied',
            form.errors.get('__all__'))

    def test_mother_Sero_Positive_perinatally_infected_not_applicable(self):
        """the mother is HIV sero positive but the the field for whether she is perinatally infected is not
           applicable"""
        self.options.update(sero_positive=YES, perinataly_infected=NOT_APPLICABLE)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'The field for whether the mother is perinataly_infected should not be N/A',
            form.errors.get('__all__'))

    def test_mother_sero_positive_anyone_know_mother_HIV_status(self):
        """The mother is HIV Positive so the field for whether anyone knows her status should not be not applicable"""
        self.options.update(know_hiv_status=NOT_APPLICABLE)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'The field for whether anyone knows the HIV status of the mother should not be N/A',
            form.errors.get('__all__'))

    def test_mother_positive_lowest_cd4_not_applicable(self):
        """The mother is hiv sero positive, the field for whether the lowest cd4 count is known should not be N/A"""
        self.options.update(lowest_cd4_known=NOT_APPLICABLE)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'The Mother is HIV Positive, the field for whether the lowest CD4 count is known should not be N/A',
            form.errors.get('__all__'))

    def test_mother_positive_lowest_cd4_count_known_value_not_given(self):
        """The mother is HIV sero-positive and the lowest cd4 count is known but it has not been supplied"""
        self.options.update(cd4_count=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mothers lowest CD4 count is known, therefore the lowest CD4 count field should be supplied',
                      form.errors.get('__all__'))

    def test_mother_positive_lowest_cd4_count_known_date_not_given(self):
        """The mother is HIV sero-positive but the date for the cd4 test has not been supplied"""
        self.options.update(cd4_date=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mothers lowest CD4 count is known, therefore the date for the CD4 test should be supplied',
                      form.errors.get('__all__'))

    def test_mother_positive_lowest_cd4_count_known_is_date_estimated_none(self):
        """The mother is hiv sero positive and the lowest cd4 count is known but whether the date has been estimated
           is N/A"""
        self.options.update(is_date_estimated=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'The Mothers lowest CD4 count is known, therefore the field for whether the date is estimated should not'
            ' be None',
            form.errors.get('__all__'))

    def test_mother_positive_lowest_cd4_count_not_known_value_given(self):
        """The mother is HIV sero-positive and the lowest cd4 count is not known but the value has been supplied"""
        self.options.update(lowest_cd4_known=NO)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mothers lowest CD4 count is not known, therefore the lowest CD4 count field should not'
                      ' be supplied',
                      form.errors.get('__all__'))

    def test_mother_positive_lowest_cd4_count_not_known_date_given(self):
        """The mother is HIV sero-positive and the lowest cd4 count is not known but the date has been supplied"""
        self.options.update(lowest_cd4_known=NO, cd4_count=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mothers lowest CD4 count is not known, therefore the date for the CD4 test should be blank',
                      form.errors.get('__all__'))

    def test_mother_positive_lowest_cd4_count_not_known_isdate_estimated_not_none(self):
        """The mother is HIV sero-positive and the lowest cd4 count is not known but the field for whether the da"""
        self.options.update(
            lowest_cd4_known=NO,
            cd4_count=None,
            cd4_date=None,
            is_date_estimated=NO)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mothers lowest CD4 count is not known, the field for whether the date is estimated should'
                      ' be None',
                      form.errors.get('__all__'))


class TestMaternalMedicalHistoryNegMother(ChronicAndMedicationsMixin, AntenatalVisitsMotherMixin, NegMotherMixin, TestCase):

    def test_negative_mother_chronic_since_yes_who_diagnosis_not_applicable(self):
        """The mother is HIV Negative but indicated that mother had chronic conditions prior to current pregnancy,
           and the WHO diagnosis has been indicated as NOT_APPLICABLE """
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=YES,
            who_diagnosis=NOT_APPLICABLE)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'The mother is HIV negative. Chronic_since should be NO and Who Diagnosis should be Not Applicable',
            form.errors.get('__all__'))

    def test_negative_mother_chronic_since_no_who_diagnosis_yes(self):
        """The Mother is HIV Negative yet who_diagnosis has been indicated as YES. should be NOT_APPLICABLE"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NO,
            who_diagnosis=YES)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The mother is HIV negative.Who Diagnosis should be Not Applicable',
                      form.errors.get('__all__'))

    def test_negative_mother_who_listed_not_applicable_not_there(self):
        """The mother is HIV Negative but has who diagnosis listing"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NOT_APPLICABLE,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx.id])
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question5: Participant is HIV Negative, do not give a listing, rather give N/A',
            form.errors.get('__all__'))

    def test_negative_mother_who_listed_not_applicable_there(self):
        """The mother is HIV Negative but has who diagnosis listing as well as N/A"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NOT_APPLICABLE,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx.id, self.who_dx_na.id])
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question5: Participant is HIV Negative, do not give a listing, only give N/A',
            form.errors.get('__all__'))

    def test_negative_mother_who_listed_none(self):
        """The mother is HIV Negative but has who diagnosis listing as none"""
        self.options.update(
            chronic_since=NOT_APPLICABLE,
            who_diagnosis=NOT_APPLICABLE,
            who=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'Question5: Mother has prior chronic illness, they should be listed',
            form.errors.get('__all__'))

    def test_mother_negative_seropositive_yes(self):
        """The mother is HIV negative, she cannot be HIV Sero positive"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx_na.id],
            sero_positive=YES)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mother is HIV Negative she cannot be Sero Positive', form.errors.get('__all__'))

    def test_mother_negative_seropositive_date_supplied(self):
        """The mother is HIV Negative but the date of HIV diagnosis has been supplied"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx_na.id],
            sero_positive=NO)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mother is HIV Negative, the approximate date of diagnosis should not be supplied',
                      form.errors.get('__all__'))

    def test_mother_negative_perinatally_infected_yes(self):
        """The mother is HIV Negative but the field for whether she was Perinatally infected is YES"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx_na.id],
            sero_positive=NO,
            date_hiv_diagnosis=None,
            perinataly_infected=YES)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mother is HIV Negative, the field for whether she was Perinataly Infected should be N/A',
                      form.errors.get('__all__'))

    def test_mother_negative_know_hiv_status_nobody(self):
        """The mother is HIV Negative so the field for whether anyone knows that she is positive should be N/A"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx_na.id],
            sero_positive=NO,
            date_hiv_diagnosis=None,
            perinataly_infected=NOT_APPLICABLE)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn(
            'The Mother is HIV Negative, the field for whether anyone knows the if the mother is HIV Positive'
            ' should be N/A',
            form.errors.get('__all__'))

    def test_mother_negative_lowest_cd4_yes(self):
        """The mother is HIV Negative, the field for whether the lowest cd4 count is known should be N/A"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx_na.id],
            sero_positive=NO,
            date_hiv_diagnosis=None,
            perinataly_infected=NOT_APPLICABLE,
            know_hiv_status=NOT_APPLICABLE)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mother is HIV Negative, the field for whether the lowest CD4 count is known should be N/A',
                      form.errors.get('__all__'))

    def test_mother_negative_lowest_cd4_cout_value(self):
        """The mother is HIV Negative, she can't have a lowest cd4 count"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx_na.id],
            sero_positive=NO,
            date_hiv_diagnosis=None,
            perinataly_infected=NOT_APPLICABLE,
            know_hiv_status=NOT_APPLICABLE,
            lowest_cd4_known=NOT_APPLICABLE)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mother is HIV Negative, The lowest CD4 count field should be blank',
                      form.errors.get('__all__'))

    def test_mother_negative_cd4_test_date(self):
        """The mother is HIV Negative, she can't have a cd4 count test date"""
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx_na.id],
            sero_positive=NO,
            date_hiv_diagnosis=None,
            perinataly_infected=NOT_APPLICABLE,
            cd4_date=get_utcnow().date(),
            know_hiv_status=NOT_APPLICABLE,
            lowest_cd4_known=NOT_APPLICABLE,
            cd4_count=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mother is HIV Negative, The date for the CD4 Test field should be blank',
                      form.errors.get('__all__'))

    def test_mother_negative_cd4_test_date_estimated(self):
        """The mother is HIV Negative, the field for whether the cd4 count test date is estimated should be N/A"""
        self.assertEqual(
            MaternalHivStatus(
                subject_identifier=self.subject_identifier,
                reference_datetime=self.get_maternal_visit('1000M').report_datetime).result, NEG)
        self.options.update(
            maternal_visit=self.get_maternal_visit('1000M').id,
            chronic_since=NO,
            who_diagnosis=NOT_APPLICABLE,
            who=[self.who_dx_na.id],
            sero_positive=NO,
            date_hiv_diagnosis=None,
            perinataly_infected=NOT_APPLICABLE,
            know_hiv_status=NOT_APPLICABLE,
            lowest_cd4_known=NOT_APPLICABLE,
            cd4_count=None,
            cd4_date=None)
        form = MaternalMedicalHistoryForm(data=self.options)
        self.assertIn('The Mother is HIV Negative, the field for whether the date for the CD4 test is estimate'
                      ' should be left blank', form.errors.get('__all__'))
