from django.db import models
from td_registration.models import RegisteredSubject


class MaternalAztNvpManager(models.Manager):

    def get_by_natural_key(self, azt_nvp, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(azt_nvp=azt_nvp, registered_subject=registered_subject)
