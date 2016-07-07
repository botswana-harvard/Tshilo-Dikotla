from edc_consent.forms import BaseSpecimenConsentForm

from ..models import SpecimenConsent, MaternalConsent


class SpecimenConsentForm(BaseSpecimenConsentForm):

    STUDY_CONSENT = MaternalConsent

    def clean(self):
        cleaned_data = super(SpecimenConsentForm, self).clean()
        return cleaned_data

    class Meta:
        model = SpecimenConsent
        fields = '__all__'
