from edc_appointment.models import AppointmentMixin
from edc_visit_schedule.models import Schedule, VisitDefinition
from edc_appointment.exceptions import AppointmentCreateError
from edc_appointment.models import Appointment
from edc_constants.constants import COMPLETE_APPT, NEW_APPT, IN_PROGRESS, INCOMPLETE


class TdAppointmentMixin(AppointmentMixin):

    """ Model Mixin to add methods to create appointments.

    Such models may be listed by name in the ScheduledGroup model and thus
    trigger the creation of appointments.

    """

    def create_all(self, base_appt_datetime=None, using=None,
                   visit_definitions=None, dashboard_type=None, instruction=None):
        """Creates appointments for a registered subject based on a list
        of visit definitions for the given membership form instance.

            1. this is called from a post-save signal
            2. RegisteredSubject instance is expected to exist at this point
            3. Only create for visit_instance = '0'
            4. If appointment exists, just update the appt_datetime

            visit_definition contains the schedule group which contains the membership form
        """
        appointments = []
        default_appt_type = self.get_default_appt_type(self.registered_subject)
        for visit_definition in self.visit_definitions_for_schedule(model_name=self._meta.model_name, instruction=instruction):
            if visit_definition.instruction == 'V3':
                appointment = Appointment.objects.using(using).filter(
                    registered_subject=self.registered_subject,
                    visit_definition__code=visit_definition.code,
                    visit_definition__instruction='V1',
                    appt_status__in=[COMPLETE_APPT, IN_PROGRESS, INCOMPLETE]).last()
                if not appointment:
                    appointment = self.update_or_create_appointment(
                        self.registered_subject,
                        base_appt_datetime or self.get_registration_datetime(),
                        visit_definition,
                        default_appt_type,
                        dashboard_type,
                        using)
                    try:
                        Appointment.objects.using(using).get(
                            registered_subject=self.registered_subject,
                            visit_definition__code=visit_definition.code,
                            visit_definition__instruction='V1',
                            appt_status=NEW_APPT).delete()
                    except Appointment.DoesNotExist:
                        pass
            else:
                appointment = self.update_or_create_appointment(
                    self.registered_subject,
                    base_appt_datetime or self.get_registration_datetime(),
                    visit_definition,
                    default_appt_type,
                    dashboard_type,
                    using)
            appointments.append(appointment)
        return appointments

    def schedule(self, model_name=None, group_names=None):
        """Returns the schedule for this membership_form."""
        return Schedule.objects.filter(
            membership_form__content_type_map__model=model_name, group_name__in=group_names)

    def visit_definitions_for_schedule(self, model_name=None, instruction=None):
        """Returns a visit_definition queryset for this membership form's schedule."""
        # VisitDefinition = get_model('edc_visit_schedule', 'VisitDefinition')
        schedule = self.schedule(
            model_name=model_name, group_names=self.group_names)
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
