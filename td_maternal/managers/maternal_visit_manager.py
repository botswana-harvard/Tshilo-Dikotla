from django.db import models


class MaternalVisitManager(models.Manager):

    def get_by_natural_key(self, subject_identifier, visit_code):
        return self.get(subject_identifer=subject_identifier, visit_code=visit_code)
