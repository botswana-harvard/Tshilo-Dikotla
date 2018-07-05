from django import forms

from ..models import AntenatalVisitMembership
from ..models import TdConsentVersion, MaternalConsent, MaternalEligibility


class AntenatalVisitMembershipForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(AntenatalVisitMembershipForm, self).clean()
        self.validate_current_consent_version()
        return cleaned_data

    def validate_current_consent_version(self):
        try:
            td_consent_version = TdConsentVersion.objects.get(
                maternal_eligibility=self.maternal_eligibility)
        except TdConsentVersion.DoesNotExist:
            raise forms.ValidationError(
                'Complete mother\'s consent version form before proceeding')
        else:
            try:
                MaternalConsent.objects.get(
                    maternal_eligibility=self.maternal_eligibility,
                    version=td_consent_version.version)
            except MaternalConsent.DoesNotExist:
                raise forms.ValidationError(
                    'Maternal Consent form for version {} before '
                    'proceeding'.format(td_consent_version.version))

    @property
    def maternal_eligibility(self):
        cleaned_data = self.cleaned_data
        subject_identifier = cleaned_data.get(
            'registered_subject').subject_identifier
        try:
            return MaternalEligibility.objects.get(
                registered_subject__subject_identifier=subject_identifier)
        except MaternalEligibility.DoesNotExist:
            return None

    class Meta:
        model = AntenatalVisitMembership
        fields = '__all__'
