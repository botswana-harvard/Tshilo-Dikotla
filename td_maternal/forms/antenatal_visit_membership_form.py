from django import forms

from ..models import AntenatalVisitMembership, MaternalUltraSoundInitial


class AntenatalVisitMembershipForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(AntenatalVisitMembershipForm, self).clean()
        self.clean_ultrasound_form()
        return cleaned_data

    def clean_ultrasound_form(self):
        registered_subject = self.cleaned_data['registered_subject']
        try:
            MaternalUltraSoundInitial.objects.get(maternal_visit__appointment__registered_subject=registered_subject)
        except MaternalUltraSoundInitial.DoesNotExist:
            raise forms.ValidationError('Please ensure you have filled Maternal Ultrasound Initial Form in the'
                                        ' Enrollment Visit, before continuing.')

    class Meta:
        model = AntenatalVisitMembership
        fields = '__all__'
