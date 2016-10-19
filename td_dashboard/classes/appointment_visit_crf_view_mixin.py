from td_appointment.models import Appointment


class AppointmentSubjectVisitCRFViewMixin:

    def __init__(self):
        self.subject_identifier = None
        self.show = None

    @property
    def appointments(self):
        """Returns all appointments for this registered_subject or just one
        if given a appointment_code and appointment_continuation_count.

        Could show
            one
            all
            only for this membership form category (which is the subject type)
            only those for a given membership form
            only those for a visit definition grouping
            """
        appointments = []
        if self.appointment:
            appointments = [self.appointment]
        else:
            appointments = Appointment.objects.filter(
                subject_identifier=self.subject_identifier).order_by('visit_code')
        return appointments

    @property
    def appointment(self):
        appointment_id = self.context.get('appointment_pk')
        appointment = None
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
        except Appointment.DoesNotExist:
            pass
        return appointment
