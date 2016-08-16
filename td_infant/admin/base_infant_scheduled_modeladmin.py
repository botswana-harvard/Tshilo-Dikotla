from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..models import InfantVisit


class BaseInfantScheduleModelAdmin(MembershipBaseModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(BaseInfantScheduleModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
