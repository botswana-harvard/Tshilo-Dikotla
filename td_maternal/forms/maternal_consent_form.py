from dateutil.relativedelta import relativedelta
from datetime import timedelta

from django import forms
from django.conf import settings
from django.forms.utils import ErrorList
from django.utils import timezone
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_consent.forms.base_consent_form import BaseConsentForm
from edc_constants.constants import FEMALE, OMANG, OTHER

from tshilo_dikotla.choices import STUDY_SITES

from ..models import MaternalConsent, MaternalEligibility


class MaternalConsentForm(BaseConsentForm):

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
        eligibility = cleaned_data.get('maternal_eligibility')
        if cleaned_data.get('citizen') != eligibility.has_omang:
            raise forms.ValidationError(
                "In eligibility you said has_omang is {}. Yet you wrote citizen is {}. "
                "Please correct.".format(eligibility.has_omang, cleaned_data.get('citizen')))
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
        except MaternalConsent.DoesNotExist:
            consent_age = relativedelta(timezone.now().date(), cleaned_data.get('dob')).years
        eligibility_age = cleaned_data.get('maternal_eligibility').age_in_years
        if consent_age != eligibility_age:
            raise forms.ValidationError(
                'In Maternal Eligibility you indicated the participant is {}, '
                'but age derived from the DOB is {}.'.format(eligibility_age, consent_age))

    def validate_recruit_source(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('recruit_source') == OTHER:
            if not cleaned_data.get('recruit_source_other'):
                self._errors["recruit_source_other"] = ErrorList(["Please specify how you first learnt about the study."
                                                                  ])
                raise forms.ValidationError('You indicated that mother first learnt about the study from a source other'
                                            ' than those in the list provided. Please specify source.')
        else:
            if cleaned_data.get('recruit_source_other'):
                self._errors["recruit_source_other"] = ErrorList(["Please do not specify source you first learnt about"
                                                                  " the study from."])
                raise forms.ValidationError('You CANNOT specify other source that mother learnt about the study from '
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
