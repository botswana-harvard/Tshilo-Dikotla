from django.db import models


class InfantArvProphModManager(models.Manager):

    def get_by_natural_key(self, arv_code, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantArvProph = models.get_model('mb_infant', 'InfantArvProph')
        infant_arv_proph = InfantArvProph.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(arv_codefu_dx=arv_code, infant_arv_proph=infant_arv_proph)
