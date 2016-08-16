from django.db import models


class VaccinesMissedManager(models.Manager):

    def get_by_natural_key(self, received_vaccine_name, report_datetime,
                           visit_instance, code, subject_identifier_as_pk):
        InfantFuImmunizations = models.get_model('mb_infant', 'InfantFuImmunizations')
        infant_fu_immunizations = InfantFuImmunizations.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(received_vaccine_name=received_vaccine_name, infant_fu_immunizations=infant_fu_immunizations)


class VaccinesReceivedManager(models.Manager):

    def get_by_natural_key(self, missed_vaccine_name, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantFuImmunizations = models.get_model('mb_infant', 'InfantFuImmunizations')
        infant_fu_immunizations = InfantFuImmunizations.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(missed_vaccine_name=missed_vaccine_name, infant_fu_immunizations=infant_fu_immunizations)
