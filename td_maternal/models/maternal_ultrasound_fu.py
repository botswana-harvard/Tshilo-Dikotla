from .base_ultra_sound_model import BaseUtraSoundModel


class MaternalUltraSoundFu(BaseUtraSoundModel):

    ADMIN_SITE_NAME = 'td_maternal_admin'

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Ultra Sound Follow Up"
