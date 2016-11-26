from td.admin_mixins import ModelAdminMixin

from ..models import InfantVisit


class CrfModelAdminMixin(ModelAdminMixin):

    instructions = (
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'infant_visit' and request.GET.get('infant_visit'):
            kwargs["queryset"] = InfantVisit.objects.filter(pk=request.GET.get('infant_visit', 0))
        return super(CrfModelAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)
