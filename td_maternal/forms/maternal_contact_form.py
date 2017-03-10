from django import forms

from edc_constants.constants import YES
from ..models import MaternalContact, MaternalLocator


class MaternalContactForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(MaternalContactForm, self).clean()
        self.validate_maternal_locator()
        self.validate_contact_success()
        return cleaned_data

    def validate_maternal_locator(self):
        cleaned_data = self.cleaned_data
        subject_identifier = cleaned_data.get('registered_subject').subject_identifier
        try:
            locator = MaternalLocator.objects.get(
                registered_subject__subject_identifier=subject_identifier)

            if cleaned_data.get('contact_type') in ['voice_call', 'text_message']:
                if locator.may_follow_up not in [YES]:
                    raise forms.ValidationError(
                        'Maternal Locator says may_follow_up: {}, you cannot call '
                        'participant if they did not give permission.'.format(locator.may_follow_up))
                if locator.may_sms_follow_up not in [YES]:
                    raise forms.ValidationError(
                        'Maternal Locator says may_sms_follow_up: {}, you cannot sms '
                        'participant if they did not give permission.'.format(locator.may_sms_follow_up))
        except MaternalLocator.DoesNotExist:
            raise forms.ValidationError(
                'Please complete the Locator form before adding contact record.')

    def validate_contact_success(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('contact_success') == YES:
            if not cleaned_data.get('contact_comment'):
                raise forms.ValidationError('Please give the outcome of the contact with the participant.')

    class Meta:
        model = MaternalContact
        fields = '__all__'
