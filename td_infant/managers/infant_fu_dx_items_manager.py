from django.db import models


class InfantFuDxItemsManager(models.Manager):

    def get_by_natural_key(self, fu_dx, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantFuDx = models.get_model('mb_infant', 'InfantFuDxItems')
        infant_fu_dx = InfantFuDx.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(fu_dx=fu_dx, congenital_anomalies=infant_fu_dx)
