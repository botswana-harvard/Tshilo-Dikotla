from django import forms
from django.apps import apps

from edc_constants.constants import NEG, YES, NOT_APPLICABLE, POS, NO
from edc_registration.models import RegisteredSubject

from .base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalMedicalHistory, AntenatalEnrollment, PostnatalEnrollment

from tshilo_dikotla.apps.td_maternal.classes import MaternalStatusHelper


class MaternalMedicalHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalMedicalHistoryForm, self).clean()
#         if 'chronic' in cleaned_data.keys():
#             self.validate_m2m(
#                 label='chronic condition',
#                 leading=cleaned_data.get('chronic_since'),
#                 m2m=cleaned_data.get('chronic'),
#                 other=cleaned_data.get('chronic_other'))
#         # WHO validations
#         if 'who' in cleaned_data.keys():
#             self.validate_m2m_wcs_dx(
#                 label='WHO diagnoses',
#                 leading=cleaned_data.get('who_diagnosis'),
#                 m2m=cleaned_data.get('who'))
#
#         self.who_stage_diagnosis_for_neg_and_pos_mother()

        self.validate_chronic_since_who_diagnosis_neg()
        self.validate_chronic_since_who_diagnosis_pos()
        self.validate_who_diagnosis_who_chronic_list()
        self.validate_who_listing_for_neg_mother()
        self.validate_positive_mother_seropositive_yes()
        self.validate_positive_mother_seropositive_yes_cd4_known_yes()
        self.validate_positive_mother_seropositive_yes_cd4_known_no()
        self.validate_negative_mother_seropositive_no()
        self.validate_negative_mother_seropositive_no_cd4_not()
        return cleaned_data

    def validate_chronic_since_who_diagnosis_neg(self):
        cleaned_data = self.cleaned_data
        try:
            status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
            subject_status = status_helper.hiv_status

            if cleaned_data.get('chronic_since') == YES and subject_status == NEG:
                if (cleaned_data.get('who_diagnosis') == NO or cleaned_data.get('who_diagnosis') == YES or
                   cleaned_data.get('who_diagnosis') == NOT_APPLICABLE):
                    raise forms.ValidationError(
                        "The mother is HIV negative. Chronic_since should be NO and Who Diagnosis should"
                        " be Not Applicable")

            if cleaned_data.get('chronic_since') == NO and subject_status == NEG:
                if cleaned_data.get('who_diagnosis') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        "The mother is HIV negative.Who Diagnosis should be Not Applicable")

        except AntenatalEnrollment.DoesNotExist:
            pass

    def validate_chronic_since_who_diagnosis_pos(self):
        cleaned_data = self.cleaned_data
        try:
            status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
            subject_status = status_helper.hiv_status

            if cleaned_data.get('chronic_since') == YES and subject_status == POS:
                if cleaned_data.get('who_diagnosis') != YES:
                    raise forms.ValidationError(
                        "The mother is HIV positive, because Chronic_since is YES and Who Diagnosis should"
                        " also be YES")

            if cleaned_data.get('chronic_since') == NO and subject_status == POS:
                if cleaned_data.get('who_diagnosis') != NO:
                    raise forms.ValidationError(
                        "The mother is HIV positive, because Chronic_since is NO and Who Diagnosis should also be NO")

        except AntenatalEnrollment.DoesNotExist:
            pass

    def validate_who_diagnosis_who_chronic_list(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('who_diagnosis') == YES:
            if not cleaned_data.get('who'):
                raise forms.ValidationError(
                    "Mother has prior chronic illness, they should be listed")

        if cleaned_data.get('who_diagnosis') == NO:
            if cleaned_data.get('who'):
                raise forms.ValidationError(
                    "You stated there are NO chronic conditions. Please correct")

    def validate_who_listing_for_neg_mother(self):
        """Confirms the HIV status of a mother and throws
        validation error on WHO stage diagnosis selection"""

        cleaned_data = self.cleaned_data
        try:
            status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
            subject_status = status_helper.hiv_status

            if subject_status == NEG:
                if cleaned_data.get('who'):
                    raise forms.ValidationError(
                        "Mother is NEG and cannot have a WHO diagnosis listing. Answer should be Not Applicable.")
        except AntenatalEnrollment.DoesNotExist:
                pass

    def validate_positive_mother_seropositive_yes(self):
        cleaned_data = self.cleaned_data
        try:
            status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
            subject_status = status_helper.hiv_status

            if subject_status == POS:
                if cleaned_data.get('sero_posetive') == YES:
                    if not cleaned_data.get('date_hiv_diagnosis'):
                        raise forms.ValidationError(
                            "The Mother is Sero-Positive, the approximate date of diagnosis should be supplied")

                    if cleaned_data.get('perinataly_infected') == NOT_APPLICABLE:
                        raise forms.ValidationError(
                            "The field for whether the mother is perinataly_infected should not be N/A")

                    if cleaned_data.get('know_hiv_status') == NOT_APPLICABLE:
                        raise forms.ValidationError(
                            "The field for whether anyone knows the HIV status of the mother should not be N/A")

                    if cleaned_data.get('lowest_cd4_known') == NOT_APPLICABLE:
                        raise forms.ValidationError(
                            "The Mother is HIV Positive, the field for whether the lowest CD4 count is known should"
                            " not be N/A")

        except AntenatalEnrollment.DoesNotExist:
                pass

    def validate_positive_mother_seropositive_yes_cd4_known_yes(self):
        cleaned_data = self.cleaned_data
        try:
            status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
            subject_status = status_helper.hiv_status

            if subject_status == POS:
                if cleaned_data.get('sero_posetive') == YES:

                    if cleaned_data.get('lowest_cd4_known') == YES and not cleaned_data.get('cd4_count'):
                        raise forms.ValidationError(
                            "The Mothers lowest CD4 count is known, therefore the lowest CD4 count field should be"
                            " supplied")

                    if cleaned_data.get('lowest_cd4_known') == YES and not cleaned_data.get('cd4_date'):
                        raise forms.ValidationError(
                            "The Mothers lowest CD4 count is known, therefore the date for the CD4 test should be"
                            " supplied")

                    if (cleaned_data.get('lowest_cd4_known') == YES and
                       cleaned_data.get('is_date_estimated') is None):
                        raise forms.ValidationError(
                            "The Mothers lowest CD4 count is known, therefore the field for whether the date is"
                            " estimated should not be None")

        except AntenatalEnrollment.DoesNotExist:
                pass

    def validate_positive_mother_seropositive_yes_cd4_known_no(self):
        cleaned_data = self.cleaned_data
        try:
            status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
            subject_status = status_helper.hiv_status

            if subject_status == POS:
                if cleaned_data.get('sero_posetive') == YES:

                    if cleaned_data.get('lowest_cd4_known') == NO and cleaned_data.get('cd4_count'):
                        raise forms.ValidationError(
                            "The Mothers lowest CD4 count is not known, therefore the lowest CD4 count field should"
                            " not be supplied")

                    if cleaned_data.get('lowest_cd4_known') == NO and cleaned_data.get('cd4_date'):
                        raise forms.ValidationError(
                            "The Mothers lowest CD4 count is not known, therefore the date for the CD4 test should"
                            " be blank")

                    if (cleaned_data.get('lowest_cd4_known') == NO and
                       cleaned_data.get('is_date_estimated') is not None):
                        raise forms.ValidationError(
                            "The Mothers lowest CD4 count is not known, the field for whether the date is estimated"
                            " should be None")

                if cleaned_data.get('sero_posetive') == NO:
                    raise forms.ValidationError("The mother is HIV Positive, The field for whether she is sero"
                                                " positive should not be NO")

        except AntenatalEnrollment.DoesNotExist:
                pass

    def validate_negative_mother_seropositive_no(self):
        cleaned_data = self.cleaned_data
        try:
            status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
            subject_status = status_helper.hiv_status

            if subject_status == NEG:
                if cleaned_data.get('sero_posetive') == YES:
                    raise forms.ValidationError(
                        "The Mother is HIV Negative she cannot be Sero Positive")
                if cleaned_data.get('date_hiv_diagnosis'):
                    raise forms.ValidationError(
                        "The Mother is HIV Negative, the approximate date of diagnosis should not be supplied")

                if cleaned_data.get('perinataly_infected') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        "The Mother is HIV Negative, the field for whether she was Perinataly Infected should be N/A")

                if cleaned_data.get('know_hiv_status') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        "The Mother is HIV Negative, the field for whether anyone knows the if the mother is HIV"
                        " Positive should be N/A")

        except AntenatalEnrollment.DoesNotExist:
                pass

    def validate_negative_mother_seropositive_no_cd4_not(self):
        cleaned_data = self.cleaned_data
        try:
            status_helper = MaternalStatusHelper(cleaned_data.get('maternal_visit'))
            subject_status = status_helper.hiv_status

            if subject_status == NEG:
                if cleaned_data.get('lowest_cd4_known') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        "The Mother is HIV Negative, the field for whether the lowest CD4 count is known should be"
                        " N/A")

                if cleaned_data.get('cd4_count'):
                    raise forms.ValidationError(
                        "The Mother is HIV Negative, The lowest CD4 count field should be blank")

                if cleaned_data.get('cd4_date'):
                    raise forms.ValidationError(
                        "The Mother is HIV Negative, The date for the CD4 Test field should be blank")

                if cleaned_data.get('is_date_estimated'):
                    raise forms.ValidationError(
                        "The Mother is HIV Negative, the field for whether the date for the CD4 test is estimate"
                        " should be left blank")

        except AntenatalEnrollment.DoesNotExist:
                pass

    class Meta:
        model = MaternalMedicalHistory
        fields = '__all__'
