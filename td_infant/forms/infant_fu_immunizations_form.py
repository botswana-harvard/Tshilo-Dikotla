from django import forms

from edc_constants.constants import YES

from ..models import InfantFuImmunizations, VaccinesReceived, VaccinesMissed

from .base_infant_model_form import BaseInfantModelForm


class InfantFuImmunizationsForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFuImmunizationsForm, self).clean()
        self.validate_received_vaccine_table()
        self.validate_missed_vaccine_table()
        return cleaned_data

    def validate_received_vaccine_table(self):
        cleaned_data = self.cleaned_data
        vaccine_table = self.data.get('vaccinesreceived_set-0-received_vaccine_name')
        if cleaned_data.get('vaccines_received') == YES:
            if not vaccine_table:
                raise forms.ValidationError("You mentioned that vaccines where received. Please"
                                            " indicate which ones on the Received Vaccines table.")
        else:
            if vaccine_table:
                raise forms.ValidationError('No vaccines received. Do not fill Received Vaccines'
                                            ' table')

    def validate_missed_vaccine_table(self):
        cleaned_data = self.cleaned_data
        missed_vaccine_table = self.data.get('vaccinesmissed_set-0-missed_vaccine_name')
        if cleaned_data.get('vaccines_missed') == YES:
            if not missed_vaccine_table:
                raise forms.ValidationError("You mentioned that the child missed some vaccines."
                                            " Please indicate which ones in the Missed Vaccines "
                                            "table.")
        else:
            if missed_vaccine_table:
                raise forms.ValidationError('No vaccines missed. Do not fill Missed Vaccines'
                                            ' table.')

    class Meta:
        model = InfantFuImmunizations
        fields = '__all__'


class VaccinesReceivedForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(VaccinesReceivedForm, self).clean()
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
        return cleaned_data

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
                                            " be admistered at 2 or 3 or 4 months ONLY.")

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


class VaccinesMissedForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(VaccinesMissedForm, self).clean()
        self.validate_missed_vaccine_fields()
        return cleaned_data

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
