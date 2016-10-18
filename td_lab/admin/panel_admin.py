from django.contrib import admin

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..models import SpecimenCollection, SpecimenCollectionItem


class PanelAdmin(MembershipBaseModelAdmin):

    list_display = ('name', 'panel_type')

    filter_horizontal = ("test_code", "aliquot_type", )

    list_filter = ('panel_type', )

admin.site.register(SpecimenCollection, PanelAdmin)
