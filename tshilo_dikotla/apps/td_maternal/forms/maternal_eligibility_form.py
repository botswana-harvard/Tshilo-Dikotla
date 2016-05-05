from django import forms
from django.forms import ModelForm

from edc_constants.constants import YES, NO

from ..models import MaternalEligibility


class MaternalEligibilityForm(ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        if cleaned_data.get('currently_pregnant') == YES and cleaned_data.get('recently_delivered') == YES:
            raise forms.ValidationError('Participant CANNOT BE BOTH: pregnant & just delivered.'
                                        ' Please Correct.')
        if cleaned_data.get("currently_pregnant") == NO and cleaned_data.get("recently_delivered") == NO:
            raise forms.ValidationError("A mother is either pregnant or she may have just delivered."
                                        " Please Correct.")
        if cleaned_data.get("recently_delivered") == YES and not cleaned_data.get("hours_delivered"):
            raise forms.ValidationError("The mother reports to have recently delivered. Enter No. hours since delivery."
                                        )
        if cleaned_data.get("currently_pregnant") == YES and cleaned_data.get("hours_delivered"):
            raise forms.ValidationError("The mother reports to still be pregnant. Hours since delivery must be blank.")
        cleaned_data = super(MaternalEligibilityForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalEligibility
        fields = '__all__'
