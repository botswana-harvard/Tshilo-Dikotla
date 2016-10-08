from django.db import models


class AppointmentManager(models.Manager):

    def get_by_natural_key(self, subject_identifer, visit_code):
        return self.get(subject_identifer=subject_identifer, visit_code=visit_code)