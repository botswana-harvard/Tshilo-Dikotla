from django.contrib import admin

from td.admin_mixins import ModelAdminMixin

from ..admin_site import td_maternal_admin
from ..forms import MaternalEligibilityLossForm
from ..models import MaternalEligibilityLoss, MaternalEligibility


@admin.register(MaternalEligibilityLoss, site=td_maternal_admin)
class MaternalEligibilityLossAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = MaternalEligibilityLossForm

    fields = ('maternal_eligibility',
              'report_datetime',
              'reason_ineligible')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_eligibility":
            if request.GET.get('maternal_eligibility'):
                kwargs["queryset"] = MaternalEligibility.objects.filter(id=request.GET.get('maternal_eligibility'))
        return super(MaternalEligibilityLossAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
