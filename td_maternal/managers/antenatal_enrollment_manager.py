from django.db import models
from edc_registration.models import RegisteredSubject


class AntenatalEnrollmentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(registered_subject=registered_subject)
