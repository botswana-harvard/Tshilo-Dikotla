from django.apps import apps
from edc_visit_tracking.models import PreviousVisitMixin


class TdPreviousVisitMixin(PreviousVisitMixin):

    def previous_visit_definition(self, visit_definition):
        """Returns the previous visit definition relative to this instance or None.

        Only selects visit definition instances for this visit model."""
        consent_obj = apps.get_model('td_maternal', 'MaternalConsent')
        visit_def_obj = apps.get_model('edc_visit_schedule', 'VisitDefinition')
        maternal_consent = consent_obj.objects.filter(
            maternal_eligibility__registered_subject__subject_identifier=self.appointment.registered_subject.subject_identifier).last()

        if maternal_consent.version == '1':
            previous_visit_definition = visit_def_obj.objects.filter(
                time_point__lt=visit_definition.time_point,
                visit_tracking_content_type_map__app_label=self._meta.app_label,
                visit_tracking_content_type_map__module_name=self._meta.model_name,
                instruction='V1').order_by(
                    'time_point', 'base_interval').last()
        elif maternal_consent.version == '3':
            previous_visit_definition = visit_def_obj.objects.filter(
                time_point__lt=visit_definition.time_point,
                visit_tracking_content_type_map__app_label=self._meta.app_label,
                visit_tracking_content_type_map__module_name=self._meta.model_name,
                instruction='V3').order_by(
                'time_point', 'base_interval').last()
        if previous_visit_definition:
            return previous_visit_definition
        return None

    class Meta:
        abstract = True
