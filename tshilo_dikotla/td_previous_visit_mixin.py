from django.apps import apps
from edc_visit_tracking.models import PreviousVisitMixin


class PreviousVisitError(Exception):
    pass


class TdPreviousVisitMixin(PreviousVisitMixin):

    def has_previous_visit_or_raise(self, exception_cls=None):
        """Returns True if the previous visit in the schedule exists or this is the first visit.

        Is by-passed if 'requires_previous_visit' is False.

        You can call this from the forms clean() method."""
        exception_cls = exception_cls or PreviousVisitError
        if self.requires_previous_visit:
            previous_visit_definition = self.previous_visit_definition(
                self.appointment.visit_definition)
            if previous_visit_definition:
                if self.previous_visit(previous_visit_definition):
                    has_previous_visit = True
                elif (self.appointment.visit_definition.time_point == 0 and
                        self.appointment.visit_definition.base_interval == 0):
                    has_previous_visit = True
                else:
                    has_previous_visit = False
                if not has_previous_visit:
                    pass

    def previous_visit_definition(self, visit_definition):
        """Returns the previous visit definition relative to this instance or None.

        Only selects visit definition instances for this visit model."""
        consent_obj = apps.get_model('td_maternal', 'MaternalConsent')

        maternal_consent = consent_obj.objects.filter(
            maternal_eligibility__registered_subject__subject_identifier=self.appointment.registered_subject.subject_identifier).last()

        if not maternal_consent:
            maternal_consent = consent_obj.objects.filter(
                maternal_eligibility__registered_subject__subject_identifier=self.appointment.registered_subject.relative_identifier).last()

        if maternal_consent.version == '1':
            previous_visit_definition = self.get_visit_definition(
                instruction='V1', visit_definition=visit_definition)
        elif maternal_consent.version == '3':
            previous_visit_definition = self.get_visit_definition(
                instruction='V1', visit_definition=visit_definition)
            if not previous_visit_definition:
                self.get_visit_definition(
                    instruction='V3', visit_definition=visit_definition)
        if previous_visit_definition:
            return previous_visit_definition
        return None

    def get_visit_definition(self, instruction, visit_definition):
        visit_def_obj = apps.get_model('edc_visit_schedule', 'VisitDefinition')

        previous_visit_definition = visit_def_obj.objects.filter(
            time_point__lt=visit_definition.time_point,
            visit_tracking_content_type_map__app_label=self._meta.app_label,
            visit_tracking_content_type_map__module_name=self._meta.model_name,
            instruction=instruction).order_by(
            'time_point', 'base_interval').last()
        return previous_visit_definition

    class Meta:
        abstract = True
