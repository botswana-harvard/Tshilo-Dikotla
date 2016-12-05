from dateutil.relativedelta import relativedelta

from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer
from django.conf import settings
from django.forms.utils import ErrorList

from edc_base.modelform_mixins import Many2ManyModelFormMixin
from edc_constants.constants import (
    YES, NO, STOPPED, CONTINUOUS, RESTARTED, NOT_APPLICABLE, FEMALE, OMANG, OTHER, POS, NEG, IND, ON_STUDY)
from edc_consent.forms import BaseSpecimenConsentForm
from edc_consent.form_mixins import ConsentFormMixin
from edc_death_report.modelform_mixins import DeathReportFormMixin
from edc_locator.forms import LocatorFormMixin
from edc_offstudy.modelform_mixins import OffStudyFormMixin
from edc_pregnancy_utils import Lmp, Edd, Ultrasound
from edc_visit_tracking.choices import VISIT_REASON
from edc_visit_tracking.form_mixins import VisitFormMixin

from td.choices import STUDY_SITES, OFF_STUDY_REASON, VISIT_INFO_SOURCE, MATERNAL_VISIT_STUDY_STATUS
from td.constants import NO_MODIFICATIONS

from .enrollment_helper import EnrollmentHelper
from .maternal_hiv_status import MaternalHivStatus
from .models import (
    AntenatalEnrollment, AntenatalEnrollmentTwo, MaternalLifetimeArvHistory, MaternalConsent,
    MaternalObstericalHistory, MaternalArvPost, MaternalArvPostMed, MaternalArvPostAdh,
    MaternalArvPreg, MaternalArv, MaternalAztNvp, MaternalRando, MaternalClinicalMeasurementsOne,
    MaternalClinicalMeasurementsTwo, MaternalContraception, MaternalDeathReport, MaternalDemographics,
    MaternalDiagnoses, MaternalEligibility, MaternalEligibilityLoss, MaternalInterimIdcc, MaternalHivInterimHx,
    MaternalLabDel, MaternalVisit, MaternalLocator, MaternalMedicalHistory, MaternalUltraSoundInitial,
    MaternalOffstudy, MaternalPostPartumDep, MaternalPostPartumFu, MaternalSubstanceUseDuringPreg,
    MaternalSubstanceUsePriorPreg, MaternalUltraSoundFu, NvpDispensing, RapidTestResult, SpecimenConsent
)


class ModelFormMixin(Many2ManyModelFormMixin):

    @property
    def maternal_hiv_status(self):
        visit = self.cleaned_data.get('maternal_visit')
        return MaternalHivStatus(
            subject_identifier=visit.subject_identifier,
            reference_datetime=visit.report_datetime)


class MaternalVisitForm (VisitFormMixin, forms.ModelForm):

    participant_label = 'mother'

    study_status = forms.ChoiceField(
        label='What is the mother\'s current study status',
        choices=MATERNAL_VISIT_STUDY_STATUS,
        initial=ON_STUDY,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        required=False,
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean_ultrasound_form(self, cleaned_data):
        subject_identifier = cleaned_data['appointment'].subject_identifier
        if cleaned_data['appointment'].visit_code == '1020M':
            try:
                MaternalUltraSoundInitial.objects.get(maternal_visit__appointment__subject_identifier=subject_identifier)
            except MaternalUltraSoundInitial.DoesNotExist:
                raise forms.ValidationError('Please ensure you have filled Maternal Ultrasound Initial Form before'
                                            ' continuing.')

    def check_creation_of_antenatal_visit_2(self, cleaned_data):
        appointment = cleaned_data.get('appointment')
        if appointment.visit_code == '1020M':
            gestational_age = MaternalUltraSoundInitial.objects.get(
                maternal_visit__appointment__subject_identifier=appointment.subject_identifier)
            gestational_age = gestational_age.evaluate_ga_confirmed()
            if gestational_age < 32:
                raise forms.ValidationError('Antenatal Visit 2 cannot occur before 32 weeks. Current GA is "{}" weeks'.
                                            format(gestational_age))

    class Meta:
        model = MaternalVisit
        fields = '__all__'


class MaternalOffstudyForm (OffStudyFormMixin, ModelFormMixin, forms.ModelForm):

    reason = forms.ChoiceField(
        label='Please code the primary reason participant taken off-study',
        choices=[choice for choice in OFF_STUDY_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    class Meta:
        model = MaternalOffstudy
        fields = '__all__'


class MaternalDeathReportForm(DeathReportFormMixin, ModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalDeathReport
        fields = '__all__'


class MaternalLocatorForm(LocatorFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalLocator
        fields = '__all__'


class AntenatalEnrollmentForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(AntenatalEnrollmentForm, self).clean()
        self.validate_last_period_date(cleaned_data.get('report_datetime'), cleaned_data.get('last_period_date'))
        enrollment_helper = EnrollmentHelper(self._meta.model(**cleaned_data), exception_cls=forms.ValidationError)
        enrollment_helper.raise_validation_error_for_rapidtest()
        return cleaned_data

    def validate_last_period_date(self, report_datetime, last_period_date):
        if last_period_date and (last_period_date >= report_datetime.date() - relativedelta(weeks=4)):
                raise forms.ValidationError('LMP cannot be within 4weeks of report datetime. '
                                            'Got LMP as {} and report datetime as {}'.format(
                                                last_period_date, report_datetime))

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'


class AntenatalEnrollmentTwoForm(ModelFormMixin, forms.ModelForm):

    class Meta:
        model = AntenatalEnrollmentTwo
        fields = '__all__'


class MaternalLifetimeArvHistoryForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalLifetimeArvHistoryForm, self).clean()
        self.validate_if_not_on_haart()
        self.validate_haart_start_date()
        self.validate_prev_preg()
        return cleaned_data

    def validate_if_not_on_haart(self):
        """Confirms that HAART is not continuous or stopped if reported as not on haart."""
        cleaned_data = self.cleaned_data
        if cleaned_data.get('preg_on_haart') == NO:
            if cleaned_data.get('prior_preg') == RESTARTED:
                raise forms.ValidationError(
                    'You indicated that the mother was NOT on triple ARV when she '
                    'got pregnant. ARVs could not have been interrupted. Please correct.')
            if cleaned_data.get('prior_preg') == CONTINUOUS:
                raise forms.ValidationError(
                    'You indicated that the mother was NOT on triple ARV when she '
                    'got pregnant. ARVs could not have been uninterrupted. Please correct.')
        else:
            if cleaned_data.get('prior_preg') == STOPPED:
                raise forms.ValidationError(
                    'You indicated that the mother was still on triple ARV when '
                    'she got pregnant, yet you indicated that ARVs were interrupted '
                    'and never restarted. Please correct.')

    def validate_haart_start_date(self):
        cleaned_data = self.cleaned_data
        report_datetime = cleaned_data.get("report_datetime")
        haart_start_date = cleaned_data.get('haart_start_date')
        if cleaned_data.get('prev_preg_haart') == YES:
            if cleaned_data.get('haart_start_date'):
                if not cleaned_data.get('is_date_estimated'):
                    raise forms.ValidationError(
                        'Please answer: Is the subject\'s date of triple antiretrovirals estimated?')
                try:
                    maternal_consent = MaternalConsent.objects.get(
                        subject_identifier=cleaned_data.get(
                            'maternal_visit').appointment.subject_identifier)
                    if report_datetime < maternal_consent.consent_datetime:
                        raise forms.ValidationError("Report datetime CANNOT be before consent datetime")
                    if haart_start_date < maternal_consent.dob:
                        raise forms.ValidationError("Date of triple ARVs first started CANNOT be before DOB.")
                except MaternalConsent.DoesNotExist:
                    raise forms.ValidationError('Maternal Consent does not exist.')
            else:
                raise forms.ValidationError("Please give a valid arv initiation date.")

    def validate_prev_preg(self):
        cleaned_data = self.cleaned_data
        ob_history = MaternalObstericalHistory.objects.filter(
            maternal_visit__appointment__subject_identifier=cleaned_data.get(
                'maternal_visit').appointment.subject_identifier)
        if not ob_history:
            raise forms.ValidationError('Please fill in the Maternal Obsterical History form first.')
        else:
            if ob_history[0].prev_pregnancies == 0:
                if cleaned_data.get('prev_preg_haart') == YES:
                    if not cleaned_data.get('haart_start_date'):
                        raise forms.ValidationError('Please give date triple antiretrovirals first started.')
                if cleaned_data.get('prev_preg_azt') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'In Maternal Obsterical History form you indicated there were no previous '
                        'pregnancies. Receive AZT monotherapy in previous pregancy should be '
                        'NOT APPLICABLE')
                if cleaned_data.get('prev_sdnvp_labour') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'In Maternal Obsterical History form you indicated there were no previous '
                        'pregnancies. Single sd-NVP in labour during a prev pregnancy should '
                        'be NOT APPLICABLE')
                if cleaned_data.get('prev_preg_haart') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'In Maternal Obsterical History form you indicated there were no previous '
                        'pregnancies. triple ARVs during a prev pregnancy should '
                        'be NOT APPLICABLE')

    class Meta:
        model = MaternalLifetimeArvHistory
        fields = '__all__'


class MaternalArvPostForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvPostForm, self).clean()
        # if mother is not supposed to be on ARVS,then the MaternalArvPostAdh is not required
        if cleaned_data.get('on_arv_since') == NO or cleaned_data.get('arv_status') == 'never started':
            if MaternalArvPostAdh.objects.filter(maternal_visit=cleaned_data.get('maternal_visit')):
                raise forms.ValidationError("ARV history exists. You wrote mother did NOT receive ARVs "
                                            "in this pregnancy. Please correct '{}' first.".format(
                                                MaternalArvPostAdh._meta.verbose_name))
        if cleaned_data.get('on_arv_since') == NO and cleaned_data.get('on_arv_reason') != 'N/A':
            raise forms.ValidationError('You indicated that participant was not on HAART.'
                                        ' You CANNOT provide a reason. Please correct.')
        if cleaned_data.get('on_arv_since') == YES and cleaned_data.get('on_arv_reason') == 'N/A':
            raise forms.ValidationError("You indicated that participant was on triple ARVs. "
                                        "Reason CANNOT be 'Not Applicable'. Please correct.")
        return cleaned_data

    class Meta:
        model = MaternalArvPost
        fields = '__all__'


class MaternalArvPostMedForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvPostMedForm, self).clean()
        if (cleaned_data.get('maternal_arv_post').arv_status == NOT_APPLICABLE or
                cleaned_data.get('maternal_arv_post').arv_status == NO_MODIFICATIONS):
            if cleaned_data.get('arv_code'):
                raise forms.ValidationError(
                    "You cannot indicate arv modifaction as you indicated {} above.".format(
                        cleaned_data.get('maternal_arv_post').arv_status))
        return cleaned_data

    class Meta:
        model = MaternalArvPostMed
        fields = '__all__'


class MaternalArvPostAdhForm(ModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalArvPostAdh
        fields = '__all__'


class MaternalArvPregForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvPregForm, self).clean()
        self.validate_interrupted_medication()
        return cleaned_data

    def validate_interrupted_medication(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('is_interrupt') == YES and
                cleaned_data.get('interrupt') == NOT_APPLICABLE):
            raise forms.ValidationError('You indicated that ARVs were interrupted during pregnancy. '
                                        'Please provide a reason for interruption')
        if (cleaned_data.get('is_interrupt') == NO and
                cleaned_data.get('interrupt') != NOT_APPLICABLE):
            raise forms.ValidationError('You indicated that ARVs were NOT interrupted during '
                                        'pregnancy. You cannot provide a reason. Please correct.')

    class Meta:
        model = MaternalArvPreg
        fields = '__all__'


class MaternalArvForm(ModelFormMixin, forms.ModelForm):
    def clean(self):
        cleaned_data = super(MaternalArvForm, self).clean()
        self.validate_start_stop_date()
        self.validate_took_arv()
        self.validate_historical_and_present_arv_start_dates()
        return cleaned_data

    def validate_start_stop_date(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stop_date'):
            if cleaned_data.get('stop_date') < cleaned_data.get('start_date'):
                raise forms.ValidationError(
                    'Your stop date of {} is prior to start date of {}. '
                    'Please correct'.format(
                        cleaned_data.get('stop_date'), cleaned_data.get('start_date')))

    def validate_took_arv(self):
        cleaned_data = self.cleaned_data
        took_arv = cleaned_data.get('maternal_arv_preg').took_arv
        if took_arv == YES:
            if not cleaned_data.get('arv_code'):
                raise forms.ValidationError(
                    "You indicated that participant started ARV(s) during this "
                    "pregnancy. Please list them on 'Maternal ARV' table")
        else:
            if cleaned_data.get('arv_code'):
                raise forms.ValidationError(
                    "You indicated that ARV(s) were NOT started during this pregnancy. "
                    "You cannot provide a list. Please Correct.")

    def validate_historical_and_present_arv_start_dates(self):
        """Confirms that the ARV start date is not less than the Historical ARV start date"""
        cleaned_data = self.cleaned_data
        try:
            maternal_visit = cleaned_data.get('maternal_arv_preg').maternal_visit
            arv_history = MaternalLifetimeArvHistory.objects.get(maternal_visit=maternal_visit)
            if arv_history.haart_start_date:
                start_date = cleaned_data.get('start_date')
                if start_date < arv_history.haart_start_date:
                    raise forms.ValidationError(
                        "Your ARV start date {} in this pregnancy cannot be before your "
                        "Historical ARV date {}".format(
                            start_date, arv_history.haart_start_date))
        except MaternalLifetimeArvHistory.DoesNotExist:
            pass

    class Meta:
        model = MaternalArv
        fields = '__all__'


class MaternalAztNvpForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalAztNvpForm, self).clean()
        self.validate_randomization(cleaned_data)
        return cleaned_data

    class Meta:
        model = MaternalAztNvp
        fields = '__all__'

    def validate_randomization(self, cleaned_data):
        maternal_rando = MaternalRando.objects.get(
            subject_identifier=cleaned_data.get('maternal_visit').appointment.subject_identifier)
        if maternal_rando.rx != cleaned_data.get('azt_nvp_delivery'):
            raise forms.ValidationError('The chosen prophylaxis regiment does not match the randomized regiment. '
                                        ' Got {}, while randomization was {}'.format(cleaned_data.get('azt_nvp'),
                                                                                     maternal_rando.rx))


class MaternalClinicalMeasurementsOneForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalClinicalMeasurementsOneForm, self).clean()
        if not cleaned_data.get('systolic_bp'):
            raise forms.ValidationError('Systolic Blood Pressure field cannot be blank. Please correct')
        if not cleaned_data.get('diastolic_bp'):
            raise forms.ValidationError('Diastolic Blood Pressure field cannot be blank. Please correct')
        if cleaned_data.get('systolic_bp') < cleaned_data.get('diastolic_bp'):
            raise forms.ValidationError(
                'Systolic blood pressure cannot be lower than the diastolic blood pressure.'
                ' Please correct.')
        return cleaned_data

    class Meta:
        model = MaternalClinicalMeasurementsOne
        fields = '__all__'


class MaternalClinicalMeasurementsTwoForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalClinicalMeasurementsTwoForm, self).clean()
        if not cleaned_data.get('systolic_bp'):
            raise forms.ValidationError('Systolic Blood Pressure field cannot be blank. Please correct')
        if not cleaned_data.get('diastolic_bp'):
            raise forms.ValidationError('Diastolic Blood Pressure field cannot be blank. Please correct')
        if cleaned_data.get('systolic_bp') < cleaned_data.get('diastolic_bp'):
            raise forms.ValidationError(
                'Systolic blood pressure cannot be lower than the diastolic blood pressure.'
                ' Please correct.')

        return cleaned_data

    class Meta:
        model = MaternalClinicalMeasurementsTwo
        fields = '__all__'


class MaternalConsentForm(ConsentFormMixin, forms.ModelForm):

    maternal_eligibility_reference = forms.CharField(
        label='Reference',
        required=True,
        help_text='This field is read only.',
        widget=forms.TextInput(attrs={'size': 36, 'readonly': True})
    )

    study_site = forms.ChoiceField(
        label='Study site',
        choices=STUDY_SITES,
        initial=settings.DEFAULT_STUDY_SITE,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        self.cleaned_data['gender'] = FEMALE
        cleaned_data = super(MaternalConsentForm, self).clean()
        if cleaned_data.get('identity_type') == OMANG and cleaned_data.get('identity')[4] != '2':
            raise forms.ValidationError('Identity provided indicates participant is Male. Please correct.')
        self.validate_eligibility_age()
        self.validate_recruit_source()
        self.validate_recruitment_clinic()
        return cleaned_data

    def validate_eligibility_age(self):
        cleaned_data = self.cleaned_data
        try:
            identity = cleaned_data.get('identity')
            consent_v1 = MaternalConsent.objects.get(identity=identity, version=1)
            consent_age = relativedelta(consent_v1.consent_datetime.date(), consent_v1.dob).years
            print(consent_age, "consent_age, consent_age, consent_age")
        except MaternalConsent.DoesNotExist:
            pass
#             consent_age = relativedelta(
#                 get_utcnow().date(),
#                 pytz.utc.localize(datetime.combine(cleaned_data.get('dob'), time()))).years
#         eligibility_age = cleaned_data.get('maternal_eligibility').age_in_years
#         if consent_age != eligibility_age:
#             raise forms.ValidationError(
#                 'In Maternal Eligibility you indicated the participant is {}, '
#                 'but age derived from the DOB is {}.'.format(eligibility_age, consent_age))

    def validate_recruit_source(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('recruit_source') == OTHER:
            if not cleaned_data.get('recruit_source_other'):
                self._errors["recruit_source_other"] = ErrorList(
                    ["Please specify how you first learnt about the study."])
                raise forms.ValidationError(
                    'You indicated that mother first learnt about the study from a source other'
                    ' than those in the list provided. Please specify source.')
        else:
            if cleaned_data.get('recruit_source_other'):
                self._errors["recruit_source_other"] = ErrorList(
                    ["Please do not specify source you first learnt about the study from."])
                raise forms.ValidationError(
                    'You CANNOT specify other source that mother learnt about the study from '
                    'as you already indicated {}'.format(cleaned_data.get('recruit_source')))

    def validate_recruitment_clinic(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('recruitment_clinic') == OTHER:
            if not cleaned_data.get('recruitment_clinic_other'):
                self._errors["recruitment_clinic_other"] = ErrorList(["Please specify health facility."])
                raise forms.ValidationError('You indicated that mother was recruited from a health facility other '
                                            'than that list provided. Please specify that health facility.')
        else:
            if cleaned_data.get('recruitment_clinic_other'):
                self._errors["recruitment_clinic_other"] = ErrorList(["Please do not specify health facility."])
                raise forms.ValidationError('You CANNOT specify other facility that mother was recruited from as you '
                                            'already indicated {}'.format(cleaned_data.get('recruitment_clinic')))

    class Meta:
        model = MaternalConsent
        fields = '__all__'


class MaternalContraceptionForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalContraceptionForm, self).clean()
        self.validate_more_children()
        self.validate_next_child()
        self.validate_uses_contraceptive()
        self.validate_another_pregnancy()
        self.validate_pap_smear()
        self.validate_pap_smear_result()
        return cleaned_data

    def validate_more_children(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('more_children') == YES:
            if cleaned_data.get('next_child'):
                raise forms.ValidationError(
                    'You said the client does not desire more children please do not answer '
                    'When would you like to have your next child?')

    def validate_next_child(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('more_children') == YES:
            if not cleaned_data.get('next_child'):
                raise forms.ValidationError(
                    'Participant desires more children, question on next child cannot be None.')

    def validate_uses_contraceptive(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('uses_contraceptive') == YES:
            if not cleaned_data.get('contr'):
                raise forms.ValidationError('Participant uses a contraceptive method, please select a valid method')
            if not cleaned_data.get('contraceptive_startdate'):
                raise forms.ValidationError(
                    'Participant uses a contraceptive method, please give a contraceptive startdate.')
        else:
            if cleaned_data.get('contr'):
                raise forms.ValidationError(
                    'Participant does not use a contraceptive method, no need to give a contraceptive method')
            if cleaned_data.get('contraceptive_startdate'):
                raise forms.ValidationError(
                    'Participant does not use a contraceptive method, no need to give a contraceptive startdate.')

    def validate_another_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('another_pregnancy') == YES:
            if not cleaned_data.get('pregnancy_date'):
                raise forms.ValidationError('Participant is pregnant, please give date participant found out.')
        else:
            if cleaned_data.get('pregnancy_date'):
                raise forms.ValidationError('Participant is not pregnant, do not give a date.')

    def validate_pap_smear(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('pap_smear') == YES:
            if not cleaned_data.get('pap_smear_date'):
                raise forms.ValidationError('Please give the date the pap smear was done.')
            if cleaned_data.get('pap_smear_date'):
                if not cleaned_data.get('pap_smear_estimate'):
                    raise forms.ValidationError(
                        'Pap smear date has been provided, please let us know if this date has been estimated.')
        elif cleaned_data.get('pap_smear') == NO:
            if cleaned_data.get('pap_smear_date'):
                raise forms.ValidationError('Pap smear date not known, please do not add it.')
        else:
            if (cleaned_data.get('pap_smear_date') or cleaned_data.get('pap_smear_estimate') or
               cleaned_data.get('pap_smear_result') or cleaned_data.get('pap_smear_result_status') or
               cleaned_data.get('pap_smear_result_abnormal') or cleaned_data.get('date_notified')) is not None:
                raise forms.ValidationError('Pap smear not done please do not answer questions regarding pap smear.')

    def validate_pap_smear_result(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('pap_smear_result') == YES:
            if not cleaned_data.get('pap_smear_result_status'):
                raise forms.ValidationError(
                    'Participant knows her pap smear result, please give the status of the pap smear.')
        else:
            if (cleaned_data.get('pap_smear_result_status') or cleaned_data.get('pap_smear_result_abnormal') or
               cleaned_data.get('date_notified')):
                raise forms.ValidationError(
                    'Participant pap smear result not known, no need to give pap smear status or notification date.')

    class Meta:
        model = MaternalContraception
        fields = '__all__'


class MaternalDemographicsForm(ModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalDemographics
        fields = '__all__'


class MaternalDiagnosesForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalDiagnosesForm, self).clean()
        self.validate_has_diagnoses()
        self.validate_who_dignoses()
        return cleaned_data

    def validate_has_diagnoses(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('new_diagnoses') in [YES]:
            if not cleaned_data.get('diagnoses'):
                raise forms.ValidationError('Participant has new diagnoses, please give a diagnosis.')
            if self.validate_not_applicable_in_there('diagnoses'):
                raise forms.ValidationError(
                    'New Diagnoses is Yes, diagnoses list cannot have Not Applicable. Please correct.')
        else:
            if (self.validate_not_applicable_not_there('diagnoses') or
                    self.validate_not_applicable_and_other_options('diagnoses')):
                raise forms.ValidationError(
                    'Participant does not have any new diagnoses, new diagnosis should be Not Applicable.')

    def validate_who_dignoses(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_who_dx') == YES:
            if not cleaned_data.get('who'):
                raise forms.ValidationError('WHO diagnosis is Yes, please give who diagnosis.')
            if self.validate_not_applicable_in_there('who'):
                raise forms.ValidationError(
                    'WHO Stage III/IV cannot have Not Applicable in the list. Please correct.')
        if cleaned_data.get('has_who_dx') in [NO, NOT_APPLICABLE]:
            if self.validate_not_applicable_not_there('who'):
                raise forms.ValidationError(
                    'WHO diagnoses is {}, WHO Stage III/IV should be Not Applicable.'.format(
                        cleaned_data.get('has_who_dx')))

    class Meta:
        model = MaternalDiagnoses
        fields = '__all__'


class MaternalEligibilityForm(ModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalEligibility
        fields = '__all__'


class MaternalEligibilityLossForm(ModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalEligibilityLoss
        fields = '__all__'


class MaternalInterimIdccForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalInterimIdccForm, self).clean()
        self.validate_info_since_last_visit_yes()
        self.validate_info_since_last_visit_no()
        return cleaned_data

    def validate_info_since_last_visit_yes(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('info_since_lastvisit') == YES:
            # TODO: validate when value_vl_size is none and value_vl is not answered
            if cleaned_data.get('recent_cd4'):
                if not cleaned_data.get('recent_cd4_date'):
                    raise forms.ValidationError('You specified that there is recent cd4 information available,'
                                                ' please provide the date')

            if cleaned_data.get('recent_cd4_date') and not cleaned_data.get('recent_cd4'):
                raise forms.ValidationError('You provided the date for the CD4 information but have not'
                                            ' indicated the CD4 value')

            if cleaned_data.get('value_vl'):
                if not cleaned_data.get('recent_vl_date'):
                    raise forms.ValidationError('You indicated that there was a VL value, please provide the'
                                                ' date it was determined')

            if cleaned_data.get('value_vl_size') == 'less_than' and cleaned_data.get('value_vl') != 400:
                raise forms.ValidationError('You indicated that the value of the most recent VL is less_than a number,'
                                            ' therefore the value of VL should be 400')

            if cleaned_data.get('value_vl_size') == 'greater_than' and cleaned_data.get('value_vl') != 750000:
                raise forms.ValidationError('You indicated that the value of the most recent VL is greater_than a'
                                            ' number, therefore the value of VL should be 750000')

            if(cleaned_data.get('value_vl_size') == 'equal' and (cleaned_data.get('value_vl') > 750000 or
               cleaned_data.get('value_vl') < 400)):
                raise forms.ValidationError('You indicated that the value of the most recent VL is equal to a'
                                            ' number, therefore the value of VL should be between 400 and 750000'
                                            '(inclusive of 400 and 750,000)')

    def validate_info_since_last_visit_no(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('info_since_lastvisit') == NO:
            if(cleaned_data.get('recent_cd4') or cleaned_data.get('recent_cd4_date') or
               cleaned_data.get('value_vl_size') or cleaned_data.get('value_vl') or
               cleaned_data.get('recent_vl_date') or cleaned_data.get('other_diagnoses')):
                raise forms.ValidationError(
                    'You indicated that there has not been any lab information since the last visit'
                    ' please do not answer the questions on CD4, VL and diagnoses found')

    class Meta:
        model = MaternalInterimIdcc
        fields = '__all__'


class MaternalLabDelForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalLabDelForm, self).clean()
        self.validate_valid_regimen_hiv_pos_only()
        return cleaned_data

    @property
    def maternal_hiv_status(self):
        cleaned_data = self.cleaned_data
        subject_identifier = cleaned_data['subject_identifier']
        visit = MaternalVisit.objects.filter(
            subject_identifier=subject_identifier).order_by('-created').first()
        return MaternalHivStatus(
            subject_identifier=visit.subject_identifier,
            reference_datetime=visit.report_datetime)

    def validate_valid_regimen_hiv_pos_only(self):
        cleaned_data = self.cleaned_data
        if self.maternal_hiv_status.result == POS:
            if cleaned_data.get('valid_regiment_duration') not in YES:
                raise forms.ValidationError(
                    'Participant is HIV+ valid regimen duration should be YES. Please correct.')
            if cleaned_data.get('valid_regiment_duration') == YES and not cleaned_data.get('arv_initiation_date'):
                raise forms.ValidationError(
                    'You indicated participant was on valid regimen, please give a valid arv initiation date.')
            if (cleaned_data.get('valid_regiment_duration') == YES and
                (cleaned_data.get('delivery_datetime').date() - relativedelta(weeks=4) <
                    cleaned_data.get('arv_initiation_date'))):
                raise forms.ValidationError(
                    'You indicated that the mother was on REGIMEN for a valid duration, but'
                    ' delivery date is within 4weeks of art initiation date. Please correct.')
        else:
            if cleaned_data.get('valid_regiment_duration') not in [NOT_APPLICABLE]:
                raise forms.ValidationError(
                    'Participant\'s HIV status is {}, valid regimen duration should be Not Applicable.'.format(
                        self.maternal_hiv_status.result))
            if cleaned_data.get('arv_initiation_date'):
                raise forms.ValidationError(
                    'Participant\'s HIV status is {}, arv initiation date should not filled.'.format(
                        self.maternal_hiv_status.result))

    class Meta:
        model = MaternalLabDel
        fields = '__all__'


class MaternalHivInterimHxForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalHivInterimHxForm, self).clean()
#         self.validate_cd4()
#         self.validate_viral_load()
#         self.validate_vl_result()
        return cleaned_data

    def validate_cd4(self):
        # If CD4 performed, date and result should be supplied
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_cd4') == YES:
            if not cleaned_data.get('cd4_date'):
                raise forms.ValidationError(
                    'You indicated that a CD4 count was performed. Please provide the date.')
            if not cleaned_data.get('cd4_result'):
                raise forms.ValidationError(
                    'You indicated that a CD4 count was performed. Please provide the result.')
        else:
            # If cd4 was not performed no date nor result should be provided
            if cleaned_data.get('cd4_date'):
                raise forms.ValidationError(
                    'You indicated that a CD4 count was NOT performed, yet provided a date '
                    'CD4 was performed. Please correct.')
            if cleaned_data.get('cd4_result'):
                raise forms.ValidationError(
                    'You indicated that a CD4 count was NOT performed, yet provided a CD4 '
                    'result. Please correct.')

    def validate_viral_load(self):
        # If VL performed, date and result should be supplied
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_vl') == YES:
            if not cleaned_data.get('vl_date'):
                raise forms.ValidationError(
                    'You indicated that a VL count was performed. Please provide the date.')
            if cleaned_data.get('vl_detectable') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You stated that a VL count was performed. Please indicate if it '
                    'was detectable.')
        else:
            # If VL was not performed, no VL date nor result should be supplied
            if cleaned_data.get('vl_date'):
                raise forms.ValidationError(
                    'You indicated that a VL count was NOT performed, yet provided a date VL '
                    'was performed. Please correct.')
            if cleaned_data.get('vl_result'):
                raise forms.ValidationError(
                    'You indicated that a VL count was NOT performed, yet provided a VL result'
                    ' Please correct.')
            if cleaned_data.get('vl_detectable') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You stated that a VL count was NOT performed, you CANNOT indicate if VL '
                    'was detectable.')

    def validate_vl_result(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('vl_detectable') == YES:
            if not cleaned_data.get('vl_result'):
                raise forms.ValidationError(
                    'You indicated that the VL was detectable. Provide provide VL result.')
        else:
            if cleaned_data.get('vl_result'):
                raise forms.ValidationError(
                    'You indicated that the VL was NOT detectable. you cannot provide a result.')

    class Meta:
        model = MaternalHivInterimHx
        fields = '__all__'


class MaternalMedicalHistoryForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalMedicalHistoryForm, self).clean()
        self.validate_chronic_since_who_diagnosis_neg()
        self.validate_chronic_since_who_diagnosis_pos()
        self.validate_who_diagnosis_who_chronic_list()
        self.validate_mother_father_chronic_illness_multiple_selection()
        self.validate_mother_medications_multiple_selections()
        self.validate_positive_mother_seropositive_yes()
        self.validate_positive_mother_seropositive_yes_cd4_known_yes()
        self.validate_positive_mother_seropositive_yes_cd4_known_no()
        self.validate_negative_mother_seropositive_no()
        self.validate_negative_mother_seropositive_no_cd4_not()
        return cleaned_data

    def validate_chronic_since_who_diagnosis_neg(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('chronic_since') == YES and self.maternal_hiv_status.result == NEG:
            if (cleaned_data.get('who_diagnosis') == NO or cleaned_data.get('who_diagnosis') == YES or
               cleaned_data.get('who_diagnosis') == NOT_APPLICABLE):
                raise forms.ValidationError(
                    "The mother is HIV negative. Chronic_since should be NO and Who Diagnosis should"
                    " be Not Applicable")
        if cleaned_data.get('chronic_since') == NO and self.maternal_hiv_status.result == NEG:
            if cleaned_data.get('who_diagnosis') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    "The mother is HIV negative.Who Diagnosis should be Not Applicable")

    def validate_chronic_since_who_diagnosis_pos(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('chronic_since') == YES and self.maternal_hiv_status.result == POS:
            if cleaned_data.get('who_diagnosis') != YES:
                raise forms.ValidationError(
                    "The mother is HIV positive, because Chronic_since is YES and Who Diagnosis should"
                    " also be YES")
        if cleaned_data.get('chronic_since') == NO and self.maternal_hiv_status.result == POS:
            if cleaned_data.get('who_diagnosis') != NO:
                raise forms.ValidationError(
                    "The mother is HIV positive, because Chronic_since is NO and Who Diagnosis should also be NO")

    def validate_who_diagnosis_who_chronic_list(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('who'):
            raise forms.ValidationError(
                "Question5: Mother has prior chronic illness, they should be listed")
        if cleaned_data.get('who_diagnosis') == NOT_APPLICABLE:
            if self.validate_not_applicable_not_there('who') and self.maternal_hiv_status.result == NEG:
                raise forms.ValidationError(
                    "Question5: Participant is HIV Negative, do not give a listing, rather give N/A")
            if self.validate_not_applicable_and_other_options('who'):
                raise forms.ValidationError(
                    "Question5: Participant is HIV Negative, do not give a listing, only give N/A")
        if cleaned_data.get('who_diagnosis') == YES:
            if self.validate_not_applicable_in_there('who') and self.maternal_hiv_status.result == POS:
                raise forms.ValidationError(
                    'Question5: Participant indicated that they had WHO stage III and IV, '
                    'list of diagnosis cannot be N/A')
        if cleaned_data.get('who_diagnosis') == NO:
            if self.validate_not_applicable_not_there('who') and self.maternal_hiv_status.result == POS:
                raise forms.ValidationError(
                    'Question5: The mother does not have prior who stage III and IV illnesses. Should provide N/A')
            if self.validate_not_applicable_and_other_options('who'):
                raise forms.ValidationError(
                    'Question5: The mother does not have prior who stage III and IV illnesses. '
                    'Should only provide N/A')

    def validate_mother_father_chronic_illness_multiple_selection(self):
        if self.validate_many_to_many_not_blank('mother_chronic'):
            raise forms.ValidationError(
                'Question6: The field for the chronic illnesses of the mother should not be left blank')
        if self.validate_not_applicable_and_other_options('mother_chronic'):
            raise forms.ValidationError('Question6: You cannot select options that have N/A in them')
        if self.validate_many_to_many_not_blank('father_chronic'):
            raise forms.ValidationError(
                'Question8: The field for the chronic illnesses of the father should not be left blank')
        if self.validate_not_applicable_and_other_options('father_chronic'):
            raise forms.ValidationError('Question8: You cannot select options that have N/A in them')

    def validate_mother_medications_multiple_selections(self):
        if self.validate_many_to_many_not_blank('mother_medications'):
            raise forms.ValidationError('Question10: The field for the mothers medications should not be left blank')
        if self.validate_not_applicable_and_other_options('mother_medications'):
            raise forms.ValidationError('Question10: You cannot select options that have N/A in them')

    def validate_positive_mother_seropositive_yes(self):
        cleaned_data = self.cleaned_data
        if self.maternal_hiv_status.result == POS:
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

    def validate_positive_mother_seropositive_yes_cd4_known_yes(self):
        cleaned_data = self.cleaned_data
        if self.maternal_hiv_status.result == POS:
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

    def validate_positive_mother_seropositive_yes_cd4_known_no(self):
        cleaned_data = self.cleaned_data
        if self.maternal_hiv_status.result == POS:
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

    def validate_negative_mother_seropositive_no(self):
        cleaned_data = self.cleaned_data
        if self.maternal_hiv_status.result == NEG:
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

    def validate_negative_mother_seropositive_no_cd4_not(self):
        cleaned_data = self.cleaned_data
        if self.maternal_hiv_status.result == NEG:
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

    class Meta:
        model = MaternalMedicalHistory
        fields = '__all__'


class MaternalObstericalHistoryForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalObstericalHistoryForm, self).clean()
        self.validate_less_than_24_weeks_pregnant()
        self.validate_24wks_or_more_pregnancy()
        self.validate_live_children()
        return cleaned_data

    def validate_less_than_24_weeks_pregnant(self):
        cleaned_data = self.cleaned_data
        ultrasound = self.check_mother_gestational_age()
        if not ultrasound:
            raise forms.ValidationError('Please complete the Ultrasound form first.')
        else:
            if cleaned_data.get('prev_pregnancies') == 1 and ultrasound[0].ga_confirmed < 24:
                if (
                    cleaned_data.get('pregs_24wks_or_more') != 0 or
                    cleaned_data.get('lost_before_24wks') != 0 or
                    cleaned_data.get('lost_after_24wks') != 0
                ):
                    raise forms.ValidationError(
                        'You indicated previous pregancies were {}. '
                        'Number of pregnancies at or after 24 weeks, '
                        'number of living children, '
                        'number of children lost after 24 weeks should all be zero.'.format(
                            cleaned_data.get('prev_pregnancies')))

            if cleaned_data.get('prev_pregnancies') > 1 and ultrasound[0].ga_confirmed < 24:
                sum_pregnancies = (
                    cleaned_data.get('pregs_24wks_or_more') +
                    cleaned_data.get('lost_before_24wks') +
                    cleaned_data.get('lost_after_24wks'))
                if sum_pregnancies != (cleaned_data.get('prev_pregnancies') - 1):
                    raise forms.ValidationError(
                        'The sum of Q3, Q4 and Q5 must all add up to Q2 - 1. Please correct.')

    def validate_24wks_or_more_pregnancy(self):
        cleaned_data = self.cleaned_data
        try:
            maternal_ultrasound_initial = MaternalUltraSoundInitial.objects.get(
                maternal_visit=cleaned_data.get('maternal_visit'))
            if cleaned_data.get('prev_pregnancies') > 0 and maternal_ultrasound_initial.ga_confirmed >= 24:
                sum_pregnancies = (
                    cleaned_data.get('pregs_24wks_or_more') +
                    cleaned_data.get('lost_before_24wks') +
                    cleaned_data.get('lost_after_24wks'))
                if sum_pregnancies != cleaned_data.get('prev_pregnancies'):
                    raise forms.ValidationError(
                        'The sum of Q3, Q4 and Q5 must be equal to Q2. Please correct.')
        except MaternalUltraSoundInitial.DoesNotExist:
            raise forms.ValidationError('Please complete the Ultrasound form first.')

    def validate_live_children(self):
        cleaned_data = self.cleaned_data
        sum_deliv_37_wks = (cleaned_data.get('children_deliv_before_37wks') +
                            cleaned_data.get('children_deliv_aftr_37wks'))
        sum_lost_24_wks = cleaned_data.get('lost_before_24wks') + cleaned_data.get('lost_after_24wks')
        if sum_deliv_37_wks != ((cleaned_data.get('prev_pregnancies') - 1) - sum_lost_24_wks):
            raise forms.ValidationError('The sum of Q8 and Q9 must be equal to (Q2 -1) - (Q4 + Q5). Please correct.')

    class Meta:
        model = MaternalObstericalHistory
        fields = '__all__'


class MaternalPostPartumDepForm(ModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalPostPartumDep
        fields = '__all__'


class MaternalPostPartumFuForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalPostPartumFuForm, self).clean()
        self.validate_has_diagnoses()
        self.validate_hospitalized_yes()
        self.validate_hospitalized_no()
        self.validate_who_dignoses_neg()
        self.validate_who_diagnoses_pos()
        return cleaned_data

    def validate_has_diagnoses(self):
        cleaned_data = self.cleaned_data
        if self.validate_many_to_many_not_blank('diagnoses'):
                raise forms.ValidationError('Question4: Diagnosis field should not be left empty')
        if cleaned_data.get('new_diagnoses') == NO:
            if self.validate_not_applicable_not_there('diagnoses'):
                raise forms.ValidationError(
                    'Question4: Participant has no new diagnoses, do not give a listing, rather give N/A')
            if self.validate_not_applicable_and_other_options('diagnoses'):
                raise forms.ValidationError(
                    'Question4: Participant has no new diagnoses, do not give a listing, only give N/A')
        if cleaned_data.get('new_diagnoses') == YES:
            if self.validate_not_applicable_in_there('diagnoses'):
                raise forms.ValidationError(
                    'Question4: Participant has new diagnoses, list of diagnosis cannot be N/A')

    def validate_hospitalized_yes(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('hospitalized') == YES:
            if self.validate_many_to_many_not_blank('hospitalization_reason'):
                raise forms.ValidationError(
                    'Question7: Patient was hospitalized, please give hospitalization_reason.')
            if self.validate_not_applicable_in_there('hospitalization_reason'):
                raise forms.ValidationError(
                    'Question7: Participant was hospitalized, reasons cannot be N/A')
            if not cleaned_data.get('hospitalization_days'):
                raise forms.ValidationError(
                    'Question9: The mother was hospitalized, please give number of days hospitalized')

    def validate_hospitalized_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('hospitalized') == NO:
            if self.validate_not_applicable_not_there('hospitalization_reason'):
                raise forms.ValidationError(
                    'Question7: Participant was not hospitalized, reason should be N/A')
            if self.validate_not_applicable_and_other_options('hospitalization_reason'):
                raise forms.ValidationError(
                    'Question7: Participant was not hospitalized, reason should only be N/A')
            if cleaned_data.get('hospitalization_other'):
                raise forms.ValidationError(
                    'Question8: Patient was not hospitalized, please do not give hospitalization reason.')
            if cleaned_data.get('hospitalization_days'):
                raise forms.ValidationError(
                    'Question9: Patient was not hospitalized, please do not give hospitalization days')

    def validate_who_dignoses_neg(self):
        cleaned_data = self.cleaned_data
        if self.maternal_hiv_status.result == NEG:
            if cleaned_data.get('has_who_dx') != NOT_APPLICABLE:
                raise forms.ValidationError('The mother is Negative, question 10 for WHO Stage III/IV should be N/A')
            if self.validate_many_to_many_not_blank('who'):
                raise forms.ValidationError(
                    'Question11: Participant is HIV {}, WHO Diagnosis field should be N/A'.format(
                        self.maternal_hiv_status.result))
            if self.validate_not_applicable_not_there('who'):
                raise forms.ValidationError(
                    'The mother is Negative, question 11 for WHO Stage III/IV listing should be N/A')
            if self.validate_not_applicable_and_other_options('who'):
                raise forms.ValidationError(
                    'The mother is Negative, question 11 for WHO Stage III/IV listing should only be N/A')

    def validate_who_diagnoses_pos(self):
        cleaned_data = self.cleaned_data
        if self.maternal_hiv_status.result == POS:
            if cleaned_data.get('has_who_dx') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'The mother is positive, question 10 for WHO Stage III/IV should not be N/A')
            if self.validate_many_to_many_not_blank('who'):
                raise forms.ValidationError('Question11: WHO Diagnosis field should not be left empty')
            if cleaned_data.get('has_who_dx') == YES:
                if self.validate_not_applicable_in_there('who'):
                    raise forms.ValidationError(
                        'Question 10 is indicated as YES, who listing cannot be N/A')
            if cleaned_data.get('has_who_dx') == NO:
                if self.validate_not_applicable_not_there('who'):
                    raise forms.ValidationError(
                        'Question 10 is indicated as NO, who listing should be N/A')
                if self.validate_not_applicable_and_other_options('who'):
                    raise forms.ValidationError(
                        'Question 10 is indicated as NO, who listing should only be N/A')

    class Meta:
        model = MaternalPostPartumFu
        fields = '__all__'


class MaternalRandoForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalRandoForm, self).clean()
        antenatal_enrollment = AntenatalEnrollment.objects.get(
            subject_identifier=cleaned_data.get('maternal_visit').subject_identifier)
        if antenatal_enrollment.enrollment_hiv_status != POS:
            raise forms.ValidationError('Mother must be HIV(+) to randomize.')
        return cleaned_data

    class Meta:
        model = MaternalRando
        fields = '__all__'


class MaternalSubstanceUseDuringPregForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalSubstanceUseDuringPregForm, self).clean()
        self.validate_smoked_during_pregnancy()
        self.validate_alcohol_during_pregnancy()
        self.validate_marijuana_during_preg()
        return cleaned_data

    def validate_smoked_during_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('smoked_during_pregnancy') in [YES]:
            if not cleaned_data.get('smoking_during_preg_freq'):
                raise forms.ValidationError(
                    'Participant has smoked tobacco during this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('smoking_during_preg_freq'):
                raise forms.ValidationError(
                    'Participant has never smoked tobacco during this pregnancy, please do not give a frequency.')

    def validate_alcohol_during_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('alcohol_during_pregnancy') == YES:
            if not cleaned_data.get('alcohol_during_preg_freq'):
                raise forms.ValidationError(
                    'Participant has drank alcohol during this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('alcohol_during_preg_freq'):
                raise forms.ValidationError(
                    'Participant has never drank alcohol during this pregnancy, please do not give a frequency.')

    def validate_marijuana_during_preg(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('marijuana_during_preg') == YES:
            if not cleaned_data.get('marijuana_during_preg_freq'):
                raise forms.ValidationError(
                    'Participant has smoked marijuana during this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('marijuana_during_preg_freq'):
                raise forms.ValidationError(
                    'Participant has never smoked marijuana during this pregnancy, please do not give a frequency.')

    class Meta:
        model = MaternalSubstanceUseDuringPreg
        fields = '__all__'


class MaternalSubstanceUsePriorPregForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalSubstanceUsePriorPregForm, self).clean()
        self.validate_smoked_prior_pregnancy()
        self.validate_alcohol_prior_pregnancy()
        self.validate_marijuana_prior_preg()
        return cleaned_data

    def validate_smoked_prior_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('smoked_prior_to_preg') in [YES]:
            if not cleaned_data.get('smoking_prior_preg_freq'):
                raise forms.ValidationError(
                    'Participant has smoked tobacco prior to this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('smoking_prior_preg_freq'):
                raise forms.ValidationError(
                    'Participant has never smoked tobacco prior to this pregnancy, please do not give a frequency.')

    def validate_alcohol_prior_pregnancy(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('alcohol_prior_pregnancy') == YES:
            if not cleaned_data.get('alcohol_prior_preg_freq'):
                raise forms.ValidationError(
                    'Participant has drank alcohol prior this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('alcohol_prior_preg_freq'):
                raise forms.ValidationError(
                    'Participant has never drank alcohol prior this pregnancy, please do not give a frequency.')

    def validate_marijuana_prior_preg(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('marijuana_prior_preg') == YES:
            if not cleaned_data.get('marijuana_prior_preg_freq'):
                raise forms.ValidationError(
                    'Participant has smoked marijuana prior to this pregnancy, please give a frequency.')
        else:
            if cleaned_data.get('marijuana_prior_preg_freq'):
                raise forms.ValidationError(
                    'Participant has never smoked marijuana prior to this pregnancy, please do not give a frequency.')

    class Meta:
        model = MaternalSubstanceUsePriorPreg
        fields = '__all__'


class MaternalUltraSoundFuForm(ModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalUltraSoundFu
        fields = '__all__'


class MaternalUltraSoundInitialForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalUltraSoundInitialForm, self).clean()
        antenatal_enrollment = AntenatalEnrollment.objects.get()
        lmp = Lmp(
            lmp=antenatal_enrollment.ga_by_lmp,
            reference_date=cleaned_data.get('report_datetime'))
        ultrasound = Ultrasound(
            ultrasound_date=cleaned_data.get('report_datetime'),
            ga_confirmed_weeks=cleaned_data.get('ga_by_ultrasound_wks'),
            ga_confirmed_days=cleaned_data.get('ga_by_ultrasound_days'),
            ultrasound_edd=cleaned_data.get('est_edd_ultrasound'))
        edd = Edd(lmp=lmp, ultrasound=ultrasound)
        if not edd.edd:
            raise forms.ValidationError('Cannot determine EDD.')
        return cleaned_data

    class Meta:
        model = MaternalUltraSoundInitial
        fields = '__all__'


class NvpDispensingForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(NvpDispensingForm, self).clean()
        self.validate_correct_dose()
        self.validate_week_2_dose()
        return cleaned_data

    def validate_correct_dose(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('correct_dose') == NO:
            if not cleaned_data.get('corrected_dose'):
                raise forms.ValidationError(
                    'If the correct dose was not given, please give the corrected dose.')
        else:
            if cleaned_data.get('corrected_dose'):
                raise forms.ValidationError(
                    'If the correct dose was given, please do not give the corrected dose.')

    def validate_week_2_dose(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('dose_adjustment') == YES:
            if not cleaned_data.get('week_2_dose'):
                raise forms.ValidationError(
                    'If infant came for a week 2 dose adjustment, '
                    'please give the week 2 dose.')
        else:
            if cleaned_data.get('week_2_dose'):
                raise forms.ValidationError(
                    'If infant did not come for a week 2 dose adjustment, '
                    'please do not give the week 2 dose.')

    class Meta:
        model = NvpDispensing
        fields = '__all__'


class RapidTestResultForm(ModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(RapidTestResultForm, forms.ModelForm, self).clean()
        if cleaned_data.get('rapid_test_done') == YES:
            if not cleaned_data.get('result_date'):
                raise forms.ValidationError(
                    'If a rapid test was processed, what is the date'
                    ' of the rapid test?')
            elif not cleaned_data.get('result') in [POS, NEG, IND]:
                raise forms.ValidationError(
                    'If a rapid test was processed, what is the test result?')
        else:
            if cleaned_data.get('result_date'):
                raise forms.ValidationError(
                    'If a rapid test was not processed, please do not provide the result date. '
                    'Got {}.'.format(cleaned_data.get('result_date')))
            elif cleaned_data.get('result'):
                raise forms.ValidationError(
                    'If a rapid test was not processed, please do not provide the result. '
                    'Got {}.'.format(cleaned_data.get('result')))
        return cleaned_data

    class Meta:
        model = RapidTestResult
        fields = '__all__'


class SpecimenConsentForm(BaseSpecimenConsentForm):

    STUDY_CONSENT = MaternalConsent

    class Meta:
        model = SpecimenConsent
        fields = '__all__'
