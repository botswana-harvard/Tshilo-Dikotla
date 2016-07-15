from django.db import models


class ProfileItemManager(models.Manager):

    def get_by_natural_key(self, profile_name, alpha_code, numeric_code):
        Profile = models.get_model('lab', 'Profile')
        profile = Profile.objects.get_by_natural_key(profile_name)
        AliquotType = models.get_model('lab', 'AliquotType')
        aliquot_type = AliquotType.objects.get_by_natural_key(alpha_code, numeric_code)
        return self.get(profile=profile, aliquot_type=aliquot_type)
