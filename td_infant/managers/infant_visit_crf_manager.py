from django.db import models


class InfantVisitCrfManager(models.Manager):
    """Manager for all scheduled models (those with a maternal_visit fk)."""
    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantVisit = models.get_model('mb_infant', 'InfantVisit')
        infant_visit = InfantVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(infant_visit=infant_visit)
