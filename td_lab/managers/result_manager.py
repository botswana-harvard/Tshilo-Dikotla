from django.db import models


class ResultManager(models.Manager):

    def get_by_natural_key(self, result_identifier, subject_identifier):
        return self.get(result_identifier=result_identifier, subject_identifier=subject_identifier)
