from django.db import models


class MaternalEligibilityManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        return self.get(eligibility_id=eligibility_id)
