from django.db import models


class InfantVaccinesManager(models.Manager):

    def get_by_natural_key(self, vaccination, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantVaccines = models.get_model('mb_infant', 'InfantVaccines')
        infant_birth_feed_vaccine = InfantVaccines.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(vaccination=vaccination, infant_birth_feed_vaccine=infant_birth_feed_vaccine)
