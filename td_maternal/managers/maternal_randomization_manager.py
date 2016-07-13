from django.db import models
from edc_registration.models import RegisteredSubject


class MaternalRandoManager(models.Manager):

    def get_by_natural_key(self, sid, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(sid=sid, registered_subject=registered_subject)