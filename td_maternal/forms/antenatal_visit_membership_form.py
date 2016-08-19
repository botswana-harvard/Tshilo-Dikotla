from django import forms

from ..models import AntenatalVisitMembership


class AntenatalVisitMembershipForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(AntenatalVisitMembershipForm, self).clean()
        return cleaned_data

    class Meta:
        model = AntenatalVisitMembership
        fields = '__all__'
