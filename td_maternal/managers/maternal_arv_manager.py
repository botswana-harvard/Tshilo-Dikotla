from django.db import models


class MaternalArvManager(models.Manager):

    def get_by_natural_key(self, arv_code, start_date, report_datetime, visit_instance, code, subject_identifier_as_pk):
        MaternalArvPreg = models.get_model('mb_maternal', 'MaternalArvPreg')
        maternal_arv_preg = MaternalArvPreg.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(arv_code=arv_code, start_date=start_date, maternal_arv_preg=maternal_arv_preg)
