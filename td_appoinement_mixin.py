from edc_appointment.models import AppointmentMixin
from edc_visit_schedule.models import Schedule, VisitDefinition
from edc_appointment.exceptions import AppointmentCreateError


class TdAppointmentMixin(AppointmentMixin):

    """ Model Mixin to add methods to create appointments.

    Such models may be listed by name in the ScheduledGroup model and thus
    trigger the creation of appointments.

    """

    def schedule(self, model_name=None, group_names=None):
        """Returns the schedule for this membership_form."""
        return Schedule.objects.filter(
            membership_form__content_type_map__model=model_name, group_name__in=group_names)

    def visit_definitions_for_schedule(self, model_name=None, instruction=None):
        """Returns a visit_definition queryset for this membership form's schedule."""
        # VisitDefinition = get_model('edc_visit_schedule', 'VisitDefinition')
        schedule = self.schedule(model_name=model_name, group_names=self.group_names)
        if instruction:
            visit_definitions = VisitDefinition.objects.filter(
                schedule__in=schedule, instruction=instruction).order_by('time_point')
        else:
            visit_definitions = VisitDefinition.objects.filter(
                schedule=schedule).order_by('time_point')
        if not visit_definitions:
            raise AppointmentCreateError(
                'No visit_definitions found for membership form class {0} '
                'in schedule group {1}. Expected at least one visit '
                'definition to be associated with schedule group {1}.'.format(
                    model_name, schedule))
        return visit_definitions

    class Meta:
        abstract = True
