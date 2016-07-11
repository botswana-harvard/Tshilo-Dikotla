from django.db import models
from django.apps import apps as django_apps


class MaternalEligibilityLossManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        MaternalEligibility = django_apps.get_model('td_maternal', 'MaternalEligibility')
        maternal_eligibility = MaternalEligibility.objects.get_by_natural_key(eligibility_id=eligibility_id)
        return self.get(maternal_eligibility=maternal_eligibility)
