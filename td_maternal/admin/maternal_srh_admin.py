from django.contrib import admin

from ..forms import MaternalSrhForm
from ..models import MaternalSrh

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalSrhAdmin(BaseMaternalModelAdmin):

    form = MaternalSrhForm

    radio_fields = {'seen_at_clinic': admin.VERTICAL,
                    'reason_unseen_clinic': admin.VERTICAL,
                    'is_contraceptive_initiated': admin.VERTICAL,
                    'reason_not_initiated': admin.VERTICAL}
    filter_horizontal = ('contr',)

admin.site.register(MaternalSrh, MaternalSrhAdmin)
