from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_base.modelform_mixins import Many2ManyModelFormMixin
from edc_constants.constants import NO, YES, UNKNOWN, NOT_EVALUATED, NOT_APPLICABLE, OTHER, ON_STUDY
from edc_death_report.modelform_mixins import DeathReportFormMixin
from edc_visit_tracking.form_mixins import VisitFormMixin
from edc_visit_tracking.choices import VISIT_REASON

from tshilo_dikotla.choices import VISIT_INFO_SOURCE, INFANT_VISIT_STUDY_STATUS, INFO_PROVIDER
from tshilo_dikotla.constants import MODIFIED, DISCONTINUED, NEVER_STARTED

from td.models import RegisteredSubject
from td_maternal.models import MaternalConsent

from .choices import OFF_STUDY_REASON
from .models import (
    InfantArvProph, InfantArvProphMod, InfantVisit, InfantBirthArv, InfantBirthData, InfantBirthExam,
    InfantBirthFeedingVaccine, InfantVaccines, InfantBirth,
    InfantCongenitalAnomalies, InfantCns, InfantFacialDefect,
    InfantCleftDisorder, InfantMouthUpGi,
    InfantCardioDisorder, InfantRespiratoryDefect, InfantLowerGi,
    InfantFemaleGenital, InfantMaleGenital, InfantMusculoskeletal,
    InfantTrisomies, InfantOtherAbnormalityItems, InfantSkin,
    InfantRenal, InfantDeathReport, InfantFeeding, InfantFuDx, InfantFuDxItems, InfantFu,
    InfantFuImmunizations, VaccinesReceived, VaccinesMissed, InfantFuNewMed, InfantFuNewMedItems,
    InfantFuPhysical, InfantOffStudy, SolidFoodAssessment
)


class ModelFormMixin(Many2ManyModelFormMixin):
    pass


def get_birth_arv_visit_2000(infant_identifier):
    """Check if infant was given AZT at birth"""
    try:
        visit_2000 = InfantVisit.objects.get(
            subject_identifier=infant_identifier, appointment__visit_code=2000)
        infant_birth_arv = InfantBirthArv.objects.get(infant_visit=visit_2000)
        azt_discharge_supply = infant_birth_arv.azt_discharge_supply
    except (InfantVisit.DoesNotExist, InfantBirthArv.DoesNotExist):
        azt_discharge_supply = None
    return azt_discharge_supply


class InfantArvProphForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_taking_arv_proph_no()
        self.validate_taking_arv_proph_unknown()
        self.validate_taking_arv_proph_yes()
        return cleaned_data

    def validate_taking_arv_proph_no(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_visit').appointment.subject_identifier
        if cleaned_data.get('prophylatic_nvp') == NO:
            if cleaned_data.get('arv_status') not in [NEVER_STARTED, DISCONTINUED]:
                raise forms.ValidationError(
                    'Infant was not taking prophylactic arv, prophylaxis should be Never Started or Discontinued.')
            if (cleaned_data.get('arv_status') == DISCONTINUED and
               get_birth_arv_visit_2000(infant_identifier)) in [NO, UNKNOWN]:
                    raise forms.ValidationError(
                        'The azt discharge supply in Infant birth arv was answered as NO or Unknown, '
                        'therefore Infant ARV proph in this visit cannot be permanently discontinued.')

    def validate_taking_arv_proph_unknown(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_visit').appointment.subject_identifier
        if cleaned_data.get('prophylatic_nvp') == UNKNOWN and cleaned_data.get('arv_status') not in ['modified']:
            if get_birth_arv_visit_2000(infant_identifier) not in [UNKNOWN]:
                raise forms.ValidationError(
                    'The azt discharge supply in Infant Birth arv was not answered as UNKNOWN, Q3 cannot be Unknown.')

    def validate_taking_arv_proph_yes(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('prophylatic_nvp') == YES and
           cleaned_data.get('arv_status') in [NEVER_STARTED, DISCONTINUED]):
            raise forms.ValidationError(
                'Infant has been on prophylactic arv, cannot choose Never Started or Permanently discontinued.')

    class Meta:
        model = InfantArvProph
        fields = '__all__'


class InfantArvProphModForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_proph_mod_fields()
        self.validate_infant_arv_proph_not_modified()
        self.validate_infant_arv_code()
        return cleaned_data

    def validate_proph_mod_fields(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('arv_code'):
            if not cleaned_data.get('dose_status'):
                raise forms.ValidationError('You entered an ARV Code, please give the dose status.')

            if not cleaned_data.get('modification_date'):
                raise forms.ValidationError('You entered an ARV Code, please give the modification date.')

            if not cleaned_data.get('modification_code'):
                raise forms.ValidationError('You entered an ARV Code, please give the modification reason.')

    def validate_infant_arv_proph_not_modified(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_arv_proph').arv_status != MODIFIED:
            raise forms.ValidationError("You did NOT indicate that medication was modified, so do not ENTER "
                                        "arv inline.")

    def validate_infant_arv_code(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_arv_proph').infant_visit.appointment.subject_identifier
        if (cleaned_data.get('arv_code') == 'Zidovudine' and
           get_birth_arv_visit_2000(infant_identifier) in [YES]):
            if cleaned_data.get('modification_code') in ['Initial dose']:
                raise forms.ValidationError(
                    'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
                    'AZT cannot be initiated again.')
        if get_birth_arv_visit_2000(infant_identifier) in [YES] and cleaned_data.get('arv_code') not in ['Zidovudine']:
            raise forms.ValidationError(
                'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
                'Arv Code should be AZT')

    class Meta:
        model = InfantArvProphMod
        fields = '__all__'


class InfantBirthArvForm(forms.ModelForm):

    class Meta:
        model = InfantBirthArv
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantBirthArvForm, self).clean()
        self.validate_azt_after_birth()
        self.validate_sdnvp_after_birth()
        return cleaned_data

    def validate_azt_after_birth(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('azt_after_birth') == YES:
            if not cleaned_data.get('azt_dose_date'):
                raise forms.ValidationError('Provide date of the first dose for AZT.')
            if cleaned_data.get('azt_additional_dose') == 'N/A':
                raise forms.ValidationError('Do not select Not applicable for Q6 if Q4 answer was yes.')
        else:
            if cleaned_data.get('azt_dose_date'):
                raise forms.ValidationError('Participant indicated that AZT was NOT provided. '
                                            'You cannot provide date of first dose')

    def validate_sdnvp_after_birth(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('sdnvp_after_birth') == YES:
            if not cleaned_data.get('nvp_dose_date'):
                raise forms.ValidationError('If infant has received single dose NVP then provide NVP date.')
        else:
            if cleaned_data.get('nvp_dose_date'):
                raise forms.ValidationError('Participant indicated that NVP was NOT provided. '
                                            'You cannot provide date of first dose.')


class InfantBirthDataForm(forms.ModelForm):

    class Meta:
        model = InfantBirthData
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantBirthDataForm, self).clean()
        self.validate_apgar_score(cleaned_data)
        return cleaned_data

    def validate_apgar_score(self, cleaned_data):
        if cleaned_data.get('apgar_score') == YES:
            if not cleaned_data.get('apgar_score_min_1') == 0:
                if not cleaned_data.get('apgar_score_min_1'):
                    raise forms.ValidationError('If Apgar scored performed, then you should answer At 1 minute(Q7).')
            if not cleaned_data.get('apgar_score_min_5') == 0:
                if not cleaned_data.get('apgar_score_min_5'):
                    raise forms.ValidationError('If Apgar scored performed, then you should answer At 5 minute(Q8).')
        else:
            if cleaned_data.get('apgar_score_min_1'):
                raise forms.ValidationError('If Apgar scored was NOT performed, then you should NOT answer at '
                                            '1 minute(Q7).')
            if cleaned_data.get('apgar_score_min_5'):
                raise forms.ValidationError('If Apgar scored was NOT performed, then you should NOT answer at 5 '
                                            'minute(Q8).')
            if cleaned_data.get('apgar_score_min_10'):
                raise forms.ValidationError('If Apgar scored was NOT performed, then you should NOT answer at 10 '
                                            'minute(Q9).')


class InfantBirthExamForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantBirthExamForm, self).clean()
        self.validate_report_datetime(cleaned_data, 'report_datetime')
        self.validate_general_activity(cleaned_data)
        self.validate_heent_exam(cleaned_data)
        self.validate_resp_exam(cleaned_data)
        self.validate_cardiac_exam(cleaned_data)
        self.validate_abdominal_exam(cleaned_data)
        self.validate_skin_exam(cleaned_data)
        self.validate_neuro_exam(cleaned_data)
        return cleaned_data

    def relative_identifier(self, infant_identifier):
        return RegisteredSubject.objects.get(subject_identifier=infant_identifier).relative_identifier

    def validate_report_datetime(self, cleaned_data, field):
        try:
            relative_identifier = self.relative_identifier(cleaned_data.get('infant_visit').appointment.subject_identifier)
            maternal_consent = MaternalConsent.objects.get(
                maternal_eligibility__registered_subject__subject_identifier=relative_identifier)
            if cleaned_data.get(field) < maternal_consent.consent_datetime:
                raise forms.ValidationError("{} CANNOT be before consent datetime".format(field.title()))
            if cleaned_data.get(field).date() < maternal_consent.dob:
                raise forms.ValidationError("{} CANNOT be before dob".format(field.title()))
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    def validate_general_activity(self, cleaned_data):
        if cleaned_data.get('general_activity') == 'ABNORMAL':
            if not cleaned_data.get('abnormal_activity'):
                raise forms.ValidationError('If abnormal, please specify.')
        else:
            if cleaned_data.get('abnormal_activity'):
                raise forms.ValidationError('You indicated that there was NO abnormality in general activity, yet '
                                            'specified abnormality. Please correct')

    def validate_heent_exam(self, cleaned_data):
        if cleaned_data.get('heent_exam') == YES:
            if cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'If HEENT Exam is normal, Do not answer the following Question (Q7).'
                )
        elif cleaned_data.get('heent_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'You indicated that HEENT exam was not normal. Provide answer to Q7.'
                )

    def validate_resp_exam(self, cleaned_data):
        if cleaned_data.get('resp_exam') == YES:
            if cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'If Respiratory Exam is normal, Do not answer the following Question (Q9).'
                )
        elif cleaned_data.get('resp_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Respiratory exam was not normal. Provide answer to Q9.'
                )

    def validate_cardiac_exam(self, cleaned_data):
        if cleaned_data.get('cardiac_exam') == YES:
            if cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'If Cardiac Exam is normal, Do not answer the following Question (Q11).'
                )
        elif cleaned_data.get('cardiac_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Cardiac exam was not normal. Provide answer to Q11.'
                )

    def validate_abdominal_exam(self, cleaned_data):
        if cleaned_data.get('abdominal_exam') == YES:
            if cleaned_data.get('abdominal_exam_other'):
                raise forms.ValidationError(
                    'If Abdominal Exam is normal, Do not answer the following Question (Q13).'
                )
        elif cleaned_data.get('abdominal_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('abdominal_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Abdominal exam was not normal. Provide answer to Q13.'
                )

    def validate_skin_exam(self, cleaned_data):
        if cleaned_data.get('skin_exam') == YES:
            if cleaned_data.get('skin_exam_other'):
                raise forms.ValidationError(
                    'If Skin Exam is normal, Do not answer the following Question (Q15).'
                )
        elif cleaned_data.get('skin_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('skin_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Skin exam was not normal. Provide answer to Q15.'
                )

    def validate_neuro_exam(self, cleaned_data):
        if cleaned_data.get('neurologic_exam') == YES:
            if cleaned_data.get('neuro_exam_other'):
                raise forms.ValidationError(
                    'If Neurological Exam is normal, Do not answer the following Question (Q19).'
                )
        elif cleaned_data.get('neurologic_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('neuro_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Neurological exam was not normal. Provide answer to Q19.'
                )

    class Meta:
        model = InfantBirthExam
        fields = '__all__'


class InfantBirthFeedinVaccineForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantBirthFeedinVaccineForm, self).clean()
#         self.validate_report_datetime(cleaned_data)
        return cleaned_data

    def validate_report_datetime(self, cleaned_data):
        try:
            dob = cleaned_data.get('infant_visit').appointment.registered_subject.dob
            if cleaned_data.get('report_datetime').date() < dob:
                raise forms.ValidationError(
                    'Report date {} cannot be before infant DOB of {}'.format(
                        cleaned_data.get('report_datetime').date(),
                        cleaned_data.get('infant_visit').appointment.registered_subject.dob))
            relative_identifier = cleaned_data.get(
                'infant_visit').appointment.registered_subject.relative_identifier
            maternal_consent = MaternalConsent.objects.get(
                registered_subject__subject_identifier=relative_identifier)
            if cleaned_data.get('report_datetime') < maternal_consent.consent_datetime:
                raise forms.ValidationError(
                    "Report date of {} CANNOT be before consent datetime".format(
                        cleaned_data.get('report_datetime')))
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    class Meta:
        model = InfantBirthFeedingVaccine
        fields = '__all__'


class InfantVaccinesForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantVaccinesForm, self).clean()
#         dob = cleaned_data.get('infant_birth_feed_vaccine').infant_visit.appointment.registered_subject.dob
#         if cleaned_data.get('vaccine_date') < dob:
#                 raise forms.ValidationError(
#                     'Vaccine date {} cannot be before infant DOB of {}'.format(
#                         cleaned_data.get('vaccine_date'),
#                         cleaned_data.get(
#                             'infant_birth_feed_vaccine').infant_visit.appointment.registered_subject.dob))
#         self.validate_vaccine_date()
        return cleaned_data

    def validate_vaccine_date(self):
        cleaned_data = self.cleaned_data
        try:
            subject_identifier = cleaned_data.get(
                'infant_birth_feed_vaccine').infant_visit.appointment.registered_subject.subject_identifier
            infant_birth = InfantBirth.objects.get(registered_subject__subject_identifier=subject_identifier)
            if cleaned_data.get('vaccine_date') < infant_birth.dob:
                raise forms.ValidationError('Vaccine date CANNOT be before DOB.')
        except InfantBirth.DoesNotExist:
            raise forms.ValidationError('Infant Birth does not exist.')

    class Meta:
        model = InfantVaccines
        fields = '__all__'


class InfantBirthForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantBirthForm, self).clean()
        # DOB should match delivery date
#         maternal_identifier = cleaned_data.get('registered_subject').relative_identifier
#         try:
#             maternal_lab_del = MaternalLabourDel.objects.get(
#                 maternal_visit__appointment__registered_subject__subject_identifier=maternal_identifier)
#             if not cleaned_data.get('dob', None) == maternal_lab_del.delivery_datetime.date():
#                 raise forms.ValidationError('Infant dob must match maternal delivery date of {}. You wrote {}'
#                                             .format(maternal_lab_del.delivery_datetime.date(),
#                                                     cleaned_data.get('dob')))
#             if not self.instance.id:
#                 if InfantBirth.objects.get(maternal_labour_del=maternal_lab_del):
#                     raise forms.ValidationError(
#                         "Infant birth record cannot be saved. An infant has already been "
#                         "registered for this mother.")
#         except MaternalLabourDel.DoesNotExist:
#             raise forms.ValidationError('Cannot find maternal labour and delivery form for this infant!'
#                                         ' This is not expected.')
#         except InfantBirth.DoesNotExist:
#             pass
        return cleaned_data

    class Meta:
        model = InfantBirth
        fields = '__all__'


class InfantCongenitalAnomaliesForm(forms.ModelForm):

    class Meta:
        model = InfantCongenitalAnomalies
        fields = '__all__'


class InfantCnsForm(forms.ModelForm):

    class Meta:
        model = InfantCns
        fields = '__all__'


class InfantFacialDefectForm(forms.ModelForm):

    class Meta:
        model = InfantFacialDefect
        fields = '__all__'


class InfantCleftDisorderForm(forms.ModelForm):

    class Meta:
        model = InfantCleftDisorder
        fields = '__all__'


class InfantMouthUpGiForm(forms.ModelForm):

    class Meta:
        model = InfantMouthUpGi
        fields = '__all__'


class InfantCardioDisorderForm(forms.ModelForm):

    class Meta:
        model = InfantCardioDisorder
        fields = '__all__'


class InfantRespiratoryDefectForm(forms.ModelForm):

    class Meta:
        model = InfantRespiratoryDefect
        fields = '__all__'


class InfantLowerGiForm(forms.ModelForm):

    class Meta:
        model = InfantLowerGi
        fields = '__all__'


class InfantFemaleGenitalForm(forms.ModelForm):

    class Meta:
        model = InfantFemaleGenital
        fields = '__all__'


class InfantMaleGenitalForm(forms.ModelForm):

    class Meta:
        model = InfantMaleGenital
        fields = '__all__'


class InfantRenalForm(forms.ModelForm):

    class Meta:
        model = InfantRenal
        fields = '__all__'


class InfantMusculoskeletalForm(forms.ModelForm):

    class Meta:
        model = InfantMusculoskeletal
        fields = '__all__'


class InfantSkinForm(forms.ModelForm):

    class Meta:
        model = InfantSkin
        fields = '__all__'


class InfantTrisomiesForm(forms.ModelForm):

    class Meta:
        model = InfantTrisomies
        fields = '__all__'


class InfantOtherAbnormalityItemsForm(forms.ModelForm):

    class Meta:
        model = InfantOtherAbnormalityItems
        fields = '__all__'


class InfantDeathReportForm(DeathReportFormMixin, forms.ModelForm):

    class Meta:
        model = InfantDeathReport
        fields = '__all__'


class InfantFeedingForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantFeedingForm, self).clean()
        self.validate_other_feeding()
        self.validate_took_formula()
        self.validate_took_formula_not_yes()
        self.validate_cows_milk()
        self.validate_took_other_milk()
        self.validate_breast_milk_weaning()
        self.validate_formula_intro_occur(cleaned_data)
        return cleaned_data

    def validate_other_feeding(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('formula_intro_occur') == YES:
            if not cleaned_data.get('formula_intro_date'):
                raise forms.ValidationError('Question3: If received formula milk | foods | liquids since last'
                                            ' attended visit. Please provide intro date')
        else:
            if cleaned_data.get('formula_intro_date'):
                raise forms.ValidationError('You mentioned no formula milk | foods | liquids received'
                                            ' since last visit in question 3. DO NOT PROVIDE DATE')

    def validate_took_formula(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('took_formula') == YES:
            if not cleaned_data.get('is_first_formula'):
                raise forms.ValidationError(
                    'Question7: Infant took formula, is this the first reporting of infant formula use?'
                    ' Please provide YES or NO')

            if cleaned_data.get('is_first_formula') == YES:
                if not cleaned_data.get('date_first_formula'):
                    raise forms.ValidationError('If this is a first reporting of infant formula'
                                                ' please provide date and if date is estimated')

                if not cleaned_data.get('est_date_first_formula'):
                    raise forms.ValidationError('If this is a first reporting of infant formula'
                                                ' please provide date and if date is estimated')
            if cleaned_data.get('is_first_formula') == NO:
                if cleaned_data.get('date_first_formula'):
                    raise forms.ValidationError('Question8: You mentioned that is not the first reporting of infant'
                                                ' formula PLEASE DO NOT PROVIDE DATE')
                if cleaned_data.get('est_date_first_formula'):
                    raise forms.ValidationError('Question9: You mentioned that is not the first reporting of infant'
                                                ' formula PLEASE DO NOT PROVIDE EST DATE')

    def validate_took_formula_not_yes(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('took_formula') != YES:
            if cleaned_data.get('is_first_formula'):
                raise forms.ValidationError('Question7: You mentioned that infant did not take formula,'
                                            ' PLEASE DO NOT PROVIDE FIRST FORMULA USE INFO')

            if cleaned_data.get('date_first_formula'):
                raise forms.ValidationError('Question8: You mentioned that infant did not take formula,'
                                            ' PLEASE DO NOT PROVIDE DATE OF FIRST FORMULA USE')

            if cleaned_data.get('est_date_first_formula'):
                raise forms.ValidationError('Question9: You mentioned that infant did not take formula,'
                                            ' PLEASE DO NOT PROVIDE ESTIMATED DATE OF FIRST FORMULA USE')

    def validate_cows_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cow_milk') == YES:
            if cleaned_data.get('cow_milk_yes') == 'N/A':
                raise forms.ValidationError('Question13: If infant took cows milk. Answer CANNOT be Not Applicable')
        else:
            if not cleaned_data.get('cow_milk_yes') == 'N/A':
                raise forms.ValidationError('Question13: Infant did not take cows milk. Answer is NOT APPLICABLE')

    def validate_took_other_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('other_milk') == YES:
            if not cleaned_data.get('other_milk_animal'):
                raise forms.ValidationError('Question15: The infant took milk from another animal, please specify'
                                            ' which?')
            if cleaned_data.get('milk_boiled') == NOT_APPLICABLE:
                raise forms.ValidationError('Question16:The infant took milk from another animal, answer'
                                            ' cannot be N/A')
        else:
            if cleaned_data.get('other_milk_animal'):
                raise forms.ValidationError('Question15: The infant did not take milk from any other animal, please'
                                            ' do not provide the name of the animal')

            if cleaned_data.get('milk_boiled') != NOT_APPLICABLE:
                raise forms.ValidationError('Question16: The infant did not take milk from any other animal, the'
                                            ' answer for whether the milk was boiled should be N/A')

    def validate_breast_milk_weaning(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('ever_breastfeed') == YES:
            if cleaned_data.get('complete_weaning') != NOT_APPLICABLE:
                raise forms.ValidationError('Question24: The infant has been breastfed since the last visit, The answer'
                                            ' answer should be N/A')
        else:
            if cleaned_data.get('complete_weaning') == NOT_APPLICABLE:
                raise forms.ValidationError('Question24: The infant has not been breastfed since the last visit, '
                                            'The answer should not be N/A')

    def validate_formula_intro_occur(self, cleaned_data):
        if cleaned_data.get('formula_intro_occur') == YES:
            if cleaned_data.get('formula_intro_date'):
                answer = False
                for question in ['juice', 'cow_milk', 'other_milk', 'fruits_veg',
                                 'cereal_porridge', 'solid_liquid']:
                    if cleaned_data.get(question) == YES:
                        answer = True
                        break
                if not answer:
                    raise forms.ValidationError(
                        'You should answer YES on either one of the questions about the juice, cow_milk, other milk, '
                        'fruits_veg, cereal_porridge or solid_liquid')

    class Meta:
        model = InfantFeeding
        fields = '__all__'


class InfantFuDxForm(forms.ModelForm):

    class Meta:
        model = InfantFuDx
        fields = '__all__'


class InfantFuDxItemsForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantFuDxItemsForm, self).clean()
        self.validate_health_facility()
        self.validate_reported_hospitalization()
        self.validate_other_serious_grade3or4_infection_specification()
        self.validate_other_serious_grade3or4_non_infectious_specification()
        self.validate_other_abnormallaboratory_tests_specification()
        self.validate_new_congenital_abnormality_not_previously_identified_specification()
        return cleaned_data

    def validate_reported_hospitalization(self):
        cleaned_data = self.cleaned_data
        infant_visit = cleaned_data.get('infant_fu_dx').infant_visit
        try:
            infant_fu = InfantFu.objects.get(infant_visit=infant_visit)
            was_hospitalized = infant_fu.was_hospitalized
        except InfantFu.DoesNotExist:
            was_hospitalized = None
        if was_hospitalized == NO:
            raise forms.ValidationError(
                'Question6 in Infant Follow Up is not answered YES, you cannot fill this form.')

    def validate_health_facility(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('health_facility') == NO:
            if cleaned_data.get('was_hospitalized') == YES:
                raise forms.ValidationError(
                    'You indicated that participant was hospitalized, therefore the participant '
                    'was seen at a health facility. Please correct.')

    def validate_other_serious_grade3or4_infection_specification(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fu_dx') == 'Other serious (grade 3 or 4)infection(not listed above),specify':
            if not cleaned_data.get('fu_dx_specify'):
                raise forms.ValidationError(
                    'You mentioned there is other serious (grade 3 or 4) infection, Please specify')

    def validate_other_serious_grade3or4_non_infectious_specification(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fu_dx') == 'Other serious (grade 3 or 4) non-infectious(not listed above),specify':
            if not cleaned_data.get('fu_dx_specify'):
                raise forms.ValidationError(
                    'You mentioned there is other serious (grade 3 or 4) non-infectious, Please specify')

    def validate_other_abnormallaboratory_tests_specification(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fu_dx') == (
                'Other abnormallaboratory tests(other than tests listed above ''or tests done as part of this '
                'study), specify test and result'):
            if not cleaned_data.get('fu_dx_specify'):
                raise forms.ValidationError(
                    'You mentioned there is abnormallaboratory tests, Please specify')

    def validate_new_congenital_abnormality_not_previously_identified_specification(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fu_dx') == 'New congenital abnormality not previously identified?,specify':
            if not cleaned_data.get('fu_dx_specify'):
                raise forms.ValidationError(
                    'You mentioned there is new congenital abnormality not previously identified , Please specify')

    class Meta:
        model = InfantFuDxItems
        fields = '__all__'


class InfantFuForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super(InfantFuForm, self).clean()
        if cleaned_data.get('was_hospitalized') == YES:
            if not cleaned_data.get('days_hospitalized'):
                raise forms.ValidationError('If infant was hospitalized, please provide # of days hospitalized')
            if cleaned_data.get('days_hospitalized') > 90:
                raise forms.ValidationError('days hospitalized cannot be greater than 90days')
        return cleaned_data

    class Meta:
        model = InfantFu
        fields = '__all__'


class InfantFuImmunizationsForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantFuImmunizationsForm, self).clean()
        return cleaned_data

    class Meta:
        model = InfantFuImmunizations
        fields = '__all__'


class VaccinesReceivedForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(VaccinesReceivedForm, self).clean()
        self.validate_received_vaccine_table()
        self.validate_received_vaccine_fields()
        self.validate_vaccination_at_birth()
        self.validate_hepatitis_vaccine()
        self.validate_dpt_vaccine()
        self.validate_haemophilus_vaccine()
        self.validate_pcv_vaccine()
        self.validate_polio_vaccine()
        self.validate_rotavirus_vaccine()
        self.validate_measles_vaccine()
        self.validate_pentavalent_vaccine()
        self.validate_vitamin_a_vaccine()
        self.validate_date_not_before_birth()
        return cleaned_data

    def validate_received_vaccine_table(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_fu_immunizations').vaccines_received == YES:
            if not cleaned_data.get('received_vaccine_name'):
                raise forms.ValidationError("You mentioned that vaccines where received. Please"
                                            " indicate which ones on the Received Vaccines table.")
        else:
            if(cleaned_data.get('received_vaccine_name') or cleaned_data.get('date_given') or
               cleaned_data.get('infant_age')):
                raise forms.ValidationError('No vaccines received. Do not fill Received Vaccines'
                                            ' table')

    def get_infant_birth_date(self, infant_identifier):
            try:
                infant_birth = InfantBirth.objects.get(registered_subject__subject_identifier=infant_identifier)
                return infant_birth.dob
            except Exception as e:
                print(e)

    def validate_date_not_before_birth(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_fu_immunizations').infant_visit.subject_identifier
        infant_birth_date = self.get_infant_birth_date(infant_identifier)
        if cleaned_data.get('date_given') < infant_birth_date:
            raise forms.ValidationError("Vaccine date cannot be before infant date of birth. ")

    def validate_received_vaccine_fields(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('received_vaccine_name'):
            if not cleaned_data.get('date_given'):
                raise forms.ValidationError("You provided a vaccine name {}. "
                                            "What date was it given to the infant?".format(
                                                cleaned_data.get('received_vaccine_name')))
            if not cleaned_data.get('infant_age'):
                raise forms.ValidationError("You provided a vaccine name {}. At how many months "
                                            "was it given to the infant?".format(
                                                cleaned_data.get('received_vaccine_name')))

    def validate_vaccination_at_birth(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('received_vaccine_name') == 'BCG':
            if cleaned_data.get('infant_age') not in ['At Birth', 'After Birth']:
                raise forms.ValidationError("BCG vaccination is ONLY given at birth or few"
                                            " days after birth")

    def validate_hepatitis_vaccine(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('received_vaccine_name') == 'Hepatitis_B':
            if cleaned_data.get('infant_age') not in ['At Birth', '2', '3', '4']:
                raise forms.ValidationError("Hepatitis B can only be administered"
                                            " at birth or 2 or 3 or 4 months of infant life")

    def validate_dpt_vaccine(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('received_vaccine_name') == 'DPT':
            if cleaned_data.get('infant_age') not in ['2', '3', '4']:
                raise forms.ValidationError("DPT. Diphtheria, Pertussis and Tetanus can only"
                                            " be administered at 2 or 3 or 4 months ONLY.")

    def validate_haemophilus_vaccine(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("received_vaccine_name") == 'Haemophilus_influenza':
            if cleaned_data.get('infant_age') not in ['2', '3', '4']:
                raise forms.ValidationError("Haemophilus Influenza B vaccine can only be given "
                                            "at 2 or 3 or 4 months of infant life.")

    def validate_pcv_vaccine(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("received_vaccine_name") == 'PCV_Vaccine':
            if cleaned_data.get("infant_age") not in ['2', '3', '4']:
                raise forms.ValidationError("The PCV [Pneumonia Conjugated Vaccine], can ONLY"
                                            " be administered at 2 or 3 or 4 months of infant"
                                            " life.")

    def validate_polio_vaccine(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("received_vaccine_name") == 'Polio':
            if cleaned_data.get('infant_age') not in ['2', '3', '4', '18']:
                raise forms.ValidationError("Polio vaccine can only be administered at"
                                            " 2 or 3 or 4 or 18 months of infant life")

    def validate_rotavirus_vaccine(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("received_vaccine_name") == 'Rotavirus':
            if cleaned_data.get("infant_age") not in ['2', '3']:
                raise forms.ValidationError("Rotavirus is only administered at 2 or 3 months"
                                            " of infant life")

    def validate_measles_vaccine(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("received_vaccine_name") == 'Measles':
            if cleaned_data.get("infant_age") not in ['9', '18']:
                raise forms.ValidationError("Measles vaccine is only administered at 9 or 18"
                                            " months of infant life.")

    def validate_pentavalent_vaccine(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('received_vaccine_name') == 'Pentavalent' and
                cleaned_data.get('infant_age') not in ['2', '3', '4']):
            raise forms.ValidationError("The Pentavalent vaccine can only be administered "
                                        "at 2 or 3 or 4 months of infant life.")

    def validate_vitamin_a_vaccine(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('received_vaccine_name') == 'Vitamin_A' and
                cleaned_data.get('infant_age') != '6-11'):
            raise forms.ValidationError("Vitamin A is given to children between 6-11 months"
                                        " of life")

    class Meta:
        model = VaccinesReceived
        fields = '__all__'


class VaccinesMissedForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(VaccinesMissedForm, self).clean()
        self.validate_missed_vaccine_table()
        self.validate_missed_vaccine_fields()
        return cleaned_data

    def validate_missed_vaccine_table(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_fu_immunizations').vaccines_missed == YES:
            if not cleaned_data.get('missed_vaccine_name'):
                raise forms.ValidationError("You mentioned that the child missed some vaccines. Please"
                                            " indicate which ones in the Missed Vaccines table.")
        else:
            if(cleaned_data.get('missed_vaccine_name') or cleaned_data.get('reason_missed') or
               cleaned_data.get('reason_missed_other')):
                raise forms.ValidationError('No vaccines missed. Do not fill Missed Vaccines table')

    def validate_missed_vaccine_fields(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('missed_vaccine_name'):
            if not cleaned_data.get('reason_missed'):
                raise forms.ValidationError('You said {} vaccine was missed. Give a reason'
                                            ' for missing this vaccine'.format(
                                                cleaned_data.get('missed_vaccine_name')))

    class Meta:
        model = VaccinesMissed
        fields = '__all__'


class InfantFuNewMedForm(forms.ModelForm):

    class Meta:
        model = InfantFuNewMed
        fields = '__all__'


class InfantFuNewMedItemsForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantFuNewMedItemsForm, self).clean()
        self.validate_new_medications()
        self.validate_stop_date()
        self.validate_other()
        return cleaned_data

    def validate_new_medications(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_fu_med').new_medications == YES:
            if not cleaned_data.get('medication'):
                raise forms.ValidationError(
                    'You have indicated that participant took medications. Please provide them.')
        if cleaned_data.get('infant_fu_med').new_medications == NO:
            raise forms.ValidationError('You indicated that no medications were taken. You cannot provide the '
                                        'medication. Please correct')

    def validate_stop_date(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stop_date'):
            if cleaned_data.get('stop_date') < cleaned_data.get('date_first_medication'):
                raise forms.ValidationError('You have indicated that medication stop date is before its start date. '
                                            'Please correct.')

    def validate_other(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('medication') == OTHER and not cleaned_data.get('other_medication'):
            raise forms.ValidationError('Please specify other medication.')
        if not cleaned_data.get('medication') == OTHER and cleaned_data.get('other_medication'):
            raise forms.ValidationError('Please select Other in Medication '
                                        'in when if Other medication is being record.')

    class Meta:
        model = InfantFuNewMedItems
        fields = '__all__'


class InfantFuPhysicalForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(InfantFuPhysicalForm, self).clean()
        self.validate_height()
        self.validate_head_circum()
        self.validate_report_datetime()
        self.validate_general_activity()
        self.validate_heent_exam()
        self.validate_resp_exam()
        self.validate_cardiac_exam()
        self.validate_abdominal_exam()
        self.validate_skin_exam()
        self.validate_neuro_exam()
        return cleaned_data

    def validate_height(self):
        cleaned_data = self.cleaned_data
        visit = ['2000', '2010', '2020', '2060', '2120', '2180', '2240', '2300', '2360']

        if (not cleaned_data.get('infant_visit').appointment.visit_code == '2000' and
                not cleaned_data.get('infant_visit').appointment.visit_code == '2010'):
            prev_visit = visit.index(cleaned_data.get('infant_visit').appointment.visit_code) - 1
            while prev_visit > 0:
                try:
                    subject_identifier = cleaned_data.get('infant_visit').appointment.subject_identifier
                    prev_fu_phy = InfantFuPhysical.objects.get(
                        infant_visit__appointment__subject_identifier=subject_identifier,
                        infant_visit__appointment__visit_code=visit[prev_visit])
                    if cleaned_data.get('height') < prev_fu_phy.height:
                        raise forms.ValidationError(
                            'You stated that the height for the participant as {}, yet in visit {} '
                            'you indicated that participant height was {}. Please correct.'.format(
                                cleaned_data.get('height'), visit[prev_visit], prev_fu_phy.height))
                    break
                except InfantFuPhysical.DoesNotExist:
                    prev_visit = prev_visit - 1

    def validate_head_circum(self):
        cleaned_data = self.cleaned_data
        visit = ['2000', '2010', '2020', '2060', '2120', '2180', '2240', '2300', '2360']

        if (not cleaned_data.get('infant_visit').appointment.visit_code == '2000' and
                not cleaned_data.get('infant_visit').appointment.visit_code == '2000'):
            prev_visit = visit.index(cleaned_data.get('infant_visit').appointment.visit_code) - 1
            while prev_visit > 0:
                try:
                    subject_identifier = cleaned_data.get('infant_visit').appointment.subject_identifier
                    prev_fu_phy = InfantFuPhysical.objects.get(
                        infant_visit__appointment__subject_identifier=subject_identifier,
                        infant_visit__appointment__visit_code=visit[prev_visit])
                    if cleaned_data.get('head_circumference') < prev_fu_phy.head_circumference:
                        raise forms.ValidationError(
                            'You stated that the head circumference for the participant as {}, '
                            'yet in visit {} you indicated that participant height was {}. '
                            'Please correct.'.format(
                                cleaned_data.get('head_circumference'),
                                visit[prev_visit], prev_fu_phy.head_circumference))
                    break
                except InfantFuPhysical.DoesNotExist:
                    prev_visit = prev_visit - 1

    def validate_report_datetime(self):
        cleaned_data = self.cleaned_data
        try:
            subject_identifier = cleaned_data.get('infant_visit').appointment.subject_identifier
            infant_birth = InfantBirth.objects.get(registered_subject__subject_identifier=subject_identifier)
            if (cleaned_data.get('report_datetime').date() <
                    infant_birth.dob):
                raise forms.ValidationError('Report date {} cannot be before infant DOB of {}'.format(
                    cleaned_data.get('report_datetime').date(),
                    infant_birth.registered_subject.dob))
            maternal_consent = MaternalConsent.objects.get(
                maternal_eligibility__registered_subject__subject_identifier=infant_birth.registered_subject.relative_identifier)
            if cleaned_data.get('report_datetime') < maternal_consent.consent_datetime:
                raise forms.ValidationError(
                    "Report date of {} CANNOT be before consent datetime".format(cleaned_data.get('report_datetime')))
        except InfantBirth.DoesNotExist:
            raise forms.ValidationError('Infant Birth does not exist.')
        except MaternalConsent.DoesNotExist:
            raise forms.ValidationError('Maternal Consent does not exist.')

    def validate_general_activity(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('general_activity') == 'ABNORMAL':
            if not cleaned_data.get('abnormal_activity'):
                raise forms.ValidationError('If abnormal, please specify.')
        else:
            if cleaned_data.get('abnormal_activity'):
                raise forms.ValidationError(
                    'You indicated that there was NO abnormality in general activity, yet '
                    'specified abnormality. Please correct')

    def validate_heent_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('heent_exam') == YES:
            if cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'If HEENT Exam is normal, Do not answer the following Question (Q10).')
        elif cleaned_data.get('heent_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('heent_no_other'):
                raise forms.ValidationError(
                    'You indicated that HEENT exam was not normal. Provide answer to Q10.')

    def validate_resp_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('resp_exam') == YES:
            if cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'If Respiratory Exam is normal, Do not answer the following Question (Q12).')
        elif cleaned_data.get('resp_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('resp_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Respiratory exam was not normal. Provide answer to Q12.')

    def validate_cardiac_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cardiac_exam') == YES:
            if cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'If Cardiac Exam is normal, Do not answer the following Question (Q14).')
        elif cleaned_data.get('cardiac_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('cardiac_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Cardiac exam was not normal. Provide answer to Q14.')

    def validate_abdominal_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('abdominal_exam') == YES:
            if cleaned_data.get('abdominal_exam_other'):
                raise forms.ValidationError(
                    'If Abdominal Exam is normal, Do not answer the following Question (Q16).')
        elif cleaned_data.get('abdominal_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('abdominal_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Abdominal exam was not normal. Provide answer to Q16.')

    def validate_skin_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('skin_exam') == YES:
            if cleaned_data.get('skin_exam_other'):
                raise forms.ValidationError(
                    'If Skin Exam is normal, Do not answer the following Question (Q18).')
        elif cleaned_data.get('skin_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('skin_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Skin exam was not normal. Provide answer to Q18.')

    def validate_neuro_exam(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('neurologic_exam') == YES:
            if cleaned_data.get('neuro_exam_other'):
                raise forms.ValidationError(
                    'If Neurological Exam is normal, Do not answer the following Question (Q22).')
        elif cleaned_data.get('neurologic_exam') in [NO, NOT_EVALUATED]:
            if not cleaned_data.get('neuro_exam_other'):
                raise forms.ValidationError(
                    'You indicated that Neurological exam was not normal. Provide answer to Q22.')

    class Meta:
        model = InfantFuPhysical
        fields = '__all__'


class InfantOffStudyForm(forms.ModelForm):

    reason = forms.ChoiceField(
        label='Please code the primary reason participant taken off-study',
        choices=[choice for choice in OFF_STUDY_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    class Meta:
        model = InfantOffStudy
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantOffStudyForm, self).clean()
#         self.validate_offstudy_date()
        return cleaned_data

    def validate_offstudy_date(self):
        cleaned_data = self.cleaned_data
        maternal_subject_identifier = cleaned_data.get(
            'infant_visit').appointment.registered_subject.relative_identifier
        maternal_consent = MaternalConsent.objects.get(
            registered_subject__subject_identifier=maternal_subject_identifier)
        if cleaned_data.get('offstudy_date') < maternal_consent.consent_datetime.date():
            raise forms.ValidationError(
                'Off study date cannot be before consent date')
        if cleaned_data.get('offstudy_date') < maternal_consent.dob:
            raise forms.ValidationError(
                'Off study date cannot be before date of birth')


class InfantVisitForm(VisitFormMixin, forms.ModelForm):

    participant_label = 'infant'
    dashboard_type = 'infant'

    information_provider = forms.ChoiceField(
        label='Please indicate who provided most of the information for this infant\'s visit',
        choices=INFO_PROVIDER,
        initial='MOTHER',
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    study_status = forms.ChoiceField(
        label='What is the infant\'s current study status',
        choices=INFANT_VISIT_STUDY_STATUS,
        initial=ON_STUDY,
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        required=False,
        label='Source of information',
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    class Meta:
        model = InfantVisit
        fields = '__all__'


class SolidFoodAssessementForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(SolidFoodAssessementForm, self).clean()
        self.validate_had_any_poridge()
        self.validate_had_any_tsabana()
        self.validate_has_the_child_had_meat_chicken_or_fish()
        self.validate_has_the_child_had_any_potatoes()
        self.validate_has_had_carrot_swt_potato()
        self.validate_has_had_green_veg()
        self.validate_has_had_fresh_fruits()
        self.validate_has_had_full_cream_milk()
        self.validate_has_had_skim_milk()
        self.validate_has_had_raw_milk()
        self.validate_has_had_juice()
        self.validate_has_had_eggs()
        self.validate_has_had_yogurt()
        self.validate_has_had_cheese()
        self.validate_other_solid_food_assessment_specified()
        return cleaned_data

    def validate_had_any_poridge(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('porridge') == YES:
            if not cleaned_data.get('porridge_freq'):
                raise forms.ValidationError(
                    'Question6: Please indicate how many times this child has had porridge in the last week')

    def validate_had_any_tsabana(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('tsabana') == YES:
            if not cleaned_data.get('tsabana_week'):
                raise forms.ValidationError(
                    'Question8: Please indicate how many times this child has had tsabana in the last week')

    def validate_has_the_child_had_meat_chicken_or_fish(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('meat') == YES:
            if not cleaned_data.get('meat_freq'):
                raise forms.ValidationError(
                    'Question11: Please indicate how many times the child has had any meat, chicken or fish')

    def validate_has_the_child_had_any_potatoes(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('potatoes') == YES:
            if not cleaned_data.get('potatoes_freq'):
                raise forms.ValidationError(
                    'Question13: Please indicate how many times the child has had any potatoes')

    def validate_has_had_carrot_swt_potato(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('carrot_swt_potato') == YES:
            if not cleaned_data.get('carrot_swt_potato_freq'):
                raise forms.ValidationError(
                    'Question15: Please indicate how many times this child has had carrot, pumpkin or sweet potato')

    def validate_has_had_green_veg(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('green_veg') == YES:
            if not cleaned_data.get('green_veg_freq'):
                raise forms.ValidationError(
                    'Question17: Please indicate how many times this child has had green vegetables in the last week')

    def validate_has_had_fresh_fruits(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fresh_fruits') == YES:
            if not cleaned_data.get('fresh_fruits_freq'):
                raise forms.ValidationError(
                    'Question19: Please indicate how many times this child has had fresh fruits in the last week')

    def validate_has_had_full_cream_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('fullcream_milk') == YES:
            if not cleaned_data.get('fullcream_milk_freq'):
                raise forms.ValidationError(
                    'Question21: Please indicate how many times this child has had full cream milk in the last week')

    def validate_has_had_skim_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('skim_milk') == YES:
            if not cleaned_data.get('skim_milk_freq'):
                raise forms.ValidationError(
                    'Question23: Please indicate how many times this child has had skim milk in the last week')

    def validate_has_had_raw_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('raw_milk') == YES:
            if not cleaned_data.get('raw_milk_freq'):
                raise forms.ValidationError(
                    'Question25: Please indicate how many times this child has had raw milk in the last week')

    def validate_has_had_juice(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('juice') == YES:
            if not cleaned_data.get('juice_freq'):
                raise forms.ValidationError(
                    'Question27: Please indicate how many times this child has had juice in the last week')

    def validate_has_had_eggs(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('eggs') == YES:
            if not cleaned_data.get('eggs_freq'):
                raise forms.ValidationError(
                    'Question29: Please indicate how many times this child has had eggs in the last week')

    def validate_has_had_yogurt(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('yogurt') == YES:
            if not cleaned_data.get('yogurt_freq'):
                raise forms.ValidationError(
                    'Question31: Please indicate how many times this child has had yogurt in the last week')

    def validate_has_had_cheese(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cheese') == YES:
            if not cleaned_data.get('cheese_freq'):
                raise forms.ValidationError(
                    'Question33: Please indicate how many times this child has had Cheese in the last week')

    def validate_other_solid_food_assessment_specified(self):
        cleaned_data = self.cleaned_data
        many2many_qs = cleaned_data.get('solid_foods').values_list('short_name', flat=True)
        many2many_list = list(many2many_qs.all())
        if OTHER in many2many_list:
            raise forms.ValidationError('You selected Other foods, Please specify')

    class Meta:
        model = SolidFoodAssessment
        fields = '__all__'
