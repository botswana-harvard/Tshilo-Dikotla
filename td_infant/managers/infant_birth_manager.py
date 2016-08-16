from django.db import models


class InfantBirthModelManager(models.Manager):

    def get_by_natural_key(self, maternal_labour_del):
        return self.get(maternal_labour_del=maternal_labour_del)
