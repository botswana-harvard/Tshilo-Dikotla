from django.contrib import admin

from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin

from ..forms import SpecimenCollectionForm, SpecimenCollectionItemForm
from ..models import SpecimenCollection, SpecimenCollectionItem


@admin.register(SpecimenCollection)
class SpecimenCollectionAdmin(EdcBaseModelAdminMixin, admin.ModelAdmin):

    form = SpecimenCollectionForm
#     list_display = ('', '')
#
#     filter_horizontal = ("", "", )
#
#     list_filter = ('', )


@admin.register(SpecimenCollectionItem)
class SpecimenCollectionItemAdmin(EdcBaseModelAdminMixin, admin.ModelAdmin):

    form = SpecimenCollectionItemForm
