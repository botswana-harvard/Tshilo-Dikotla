from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin

from ..forms import MaternalEligibilityLossForm
from ..models import MaternalEligibilityLoss, MaternalEligibility


@admin.register(MaternalEligibilityLoss)
class MaternalEligibilityLossAdmin(EdcBaseModelAdminMixin, admin.ModelAdmin):

    form = MaternalEligibilityLossForm

    fields = ('maternal_eligibility',
              'report_datetime',
              'reason_ineligible')

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Eligibility",
            fields=[],
            delimiter=',',
            exclude=['user_created', 'user_modified', 'hostname_created', 'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_eligibility__registered_subject__subject_identifier',
                 'gender': 'maternal_eligibility__registered_subject__gender',
                 'dob': 'maternal_eligibility__registered_subject__dob',
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_eligibility":
            if request.GET.get('maternal_eligibility'):
                kwargs["queryset"] = MaternalEligibility.objects.filter(id=request.GET.get('maternal_eligibility'))
        return super(MaternalEligibilityLossAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
