from django.db import models


class InfantVisitCrfManager(models.Manager):
    """Manager for all scheduled models (those with a maternal_visit fk)."""

    def get_for_subject_identifier(self, subject_identifier):
        """Returns a queryset for the given subject_identifier."""
        options = {'infant_visit__appointment__subject_identifier': subject_identifier}
        return self.filter(**options)

    def get_for_visit(self, visit):
        options = {
            'infant_visit__subject_identifier': visit.subject_identifier,
            'infant_visit__appointment__visit_code': visit.appointment.visit_code}
        return self.get(**options)

    def get_by_natural_key(self, visit_code, subject_identifier):
        return self.get(subject_identifier=subject_identifier, visit_code=visit_code)
