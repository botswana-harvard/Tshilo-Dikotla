from django.db import models


class MaternalLabDelDxTManager(models.Manager):

    def get_by_natural_key(self, lab_del_dx, report_datetime, visit_instance,
                           appt_status, visit_definition_code, subject_identifier_as_pk):
        MaternalVisit = models.get_model('mb_maternal', 'MaternalVisit')
        MaternalLabDelDx = models.get_model('mb_maternal', 'MaternalLabDelDx')
        maternal_visit = MaternalVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, appt_status, visit_definition_code, subject_identifier_as_pk)
        maternal_lab_del_dx = MaternalLabDelDx.objects.get(maternal_visit=maternal_visit)
        return self.get(lab_del_dx=lab_del_dx, maternal_lab_del_dx=maternal_lab_del_dx)
