from django.db import models


class InfantFuNewMedItemsManager(models.Manager):

    def get_by_natural_key(self, medication, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantFuNewMed = models.get_model('mb_infant', 'InfantFuNewMed')
        infant_fu_med = InfantFuNewMed.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(medication=medication, infant_fu_med=infant_fu_med)
