from td.admin_mixins import ModelAdminMixin
from ..models import MaternalVisit


class BaseMaternalModelAdmin(ModelAdminMixin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('subject_identifier'):
                kwargs["queryset"] = MaternalVisit.objects.filter(
                    appointment__subject_identifier=request.GET.get('subject_identifier'),
                    appointment__visit_code=request.GET.get('visit_code'))
        return super(BaseMaternalModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
