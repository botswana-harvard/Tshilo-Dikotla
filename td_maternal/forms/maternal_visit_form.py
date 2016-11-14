from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

# from edc_base.form.old_forms import BaseModelForm
from edc_constants.constants import ON_STUDY
from edc_visit_tracking.form_mixins import VisitFormMixin
from edc_visit_tracking.choices import VISIT_REASON, MISSED_VISIT

from tshilo_dikotla.choices import VISIT_INFO_SOURCE, MATERNAL_VISIT_STUDY_STATUS

from ..models import MaternalVisit, MaternalUltraSoundInitial


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

    def get_consent(self, registered_subject):
        """Return an instance of the consent model.

        If no consent model is defined, as with infants, try for the birth_model."""
        try:
            consent = self._meta.model.consent_model.objects.get(
                subject_identifier=registered_subject.subject_identifier)
        except self._meta.model.consent_model.MultipleObjectsReturned:
            consent = self._meta.model.consent_model.objects.filter(
                subject_identifier=registered_subject.subject_identifier).order_by('version').first()
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                '\'{}\' does not exist for subject.'.format(self._meta.model.consent_model._meta.verbose_name))
        except AttributeError:
            consent = self.get_birth_model_as_consent(registered_subject)
        return consent

#     def get_birth_model_as_consent(self, registered_subject):
#         """Return the birth model in place of the consent_model."""
#         try:
#             birth_model = self._meta.model.birth_model.objects.get(
#                 subject_identifier=registered_subject.subject_identifier)
#         except ObjectDoesNotExist:
#             raise forms.ValidationError(
#                 '\'{}\' does not exist for subject.'.format(self._meta.model.consent_model._meta.verbose_name))
#         return birth_model

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
