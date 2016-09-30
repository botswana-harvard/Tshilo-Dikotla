from django.contrib import admin

from ..forms import MaternalLifetimeArvHistoryForm
from ..models import MaternalLifetimeArvHistory

from .base_maternal_model_admin import BaseMaternalModelAdmin


@admin.register(MaternalLifetimeArvHistory)
class MaternalLifetimeArvHistoryAdmin(BaseMaternalModelAdmin, admin.ModelAdmin):
    form = MaternalLifetimeArvHistoryForm

    list_display = ('maternal_visit', 'haart_start_date', 'preg_on_haart')

    list_filter = ('preg_on_haart', )

    radio_fields = {
        'prev_preg_azt': admin.VERTICAL,
        'prev_sdnvp_labour': admin.VERTICAL,
        'prev_preg_haart': admin.VERTICAL,
        'preg_on_haart': admin.VERTICAL,
        'prior_preg': admin.VERTICAL,
        'is_date_estimated': admin.VERTICAL}

    filter_horizontal = ('prior_arv', )
