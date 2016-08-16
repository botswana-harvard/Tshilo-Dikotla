from django.db import models


class MaternalArvPostModManager(models.Manager):

    def get_by_natural_key(
            self, arv_code, modification_date, report_datetime, visit_instance, appt_status,
            visit_definition_code, subject_identifier_as_pk):
        MaternalVisit = models.get_model('mb_maternal', 'MaternalVisit')
        MaternalArvPost = models.get_model('mb_maternal', 'MaternalArvPost')
        maternal_visit = MaternalVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, appt_status, visit_definition_code, subject_identifier_as_pk)
        maternal_arv_post = MaternalArvPost.objects.get(maternal_visit=maternal_visit)
        return self.get(arv_code=arv_code, modification_date=modification_date, maternal_arv_post=maternal_arv_post)
