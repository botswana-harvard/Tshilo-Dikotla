from django.db import models
from django.apps import apps as django_apps


class VisitCrfModelManager(models.Manager):

    def get_by_natural_key(self, report_datetime, visit_instance, visit_code, subject_identifier_as_pk):
        MaternalVisit = django_apps.get_model('td_maternal', 'MaternalVisit')
        maternal_visit = MaternalVisit.objects.get_by_natural_key(report_datetime,
                                                                  visit_instance,
                                                                  visit_code,
                                                                  subject_identifier_as_pk)
        return self.get(maternal_visit=maternal_visit)
