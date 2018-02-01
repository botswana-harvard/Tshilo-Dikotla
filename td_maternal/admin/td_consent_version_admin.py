from django.contrib import admin

from tshilo_dikotla.base_model_admin import BaseModelAdmin

from ..forms import TdConsentVersionForm
from ..models import TdConsentVersion, MaternalEligibility


class TdConsentVersionAdmin(BaseModelAdmin):

    dashboard_type = 'maternal'
    form = TdConsentVersionForm

    fields = ('maternal_eligibility', 'version', 'report_datetime',)
    radio_fields = {'version': admin.VERTICAL}
    list_display = ('version', 'report_datetime',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalEligibility.objects.filter(
                    id=request.GET.get('maternal_visit'))
        return super(TdConsentVersionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(TdConsentVersion, TdConsentVersionAdmin)
