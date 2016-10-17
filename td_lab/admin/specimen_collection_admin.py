from django.contrib import admin

from tshilo_dikotla.base_model_admin import MembershipBaseModelAdmin

from ..forms import SpecimenCollectionForm, SubjectConsentItemForm
from ..models import SpecimenCollection, SpecimenCollectionItem


@admin.register(SpecimenCollection)
class SpecimenCollectionAdmin(MembershipBaseModelAdmin):

    form = SpecimenCollectionForm
#     list_display = ('', '')
#
#     filter_horizontal = ("", "", )
#
#     list_filter = ('', )


@admin.register(SpecimenCollectionItem)
class SpecimenCollectionItem(MembershipBaseModelAdmin):

    form = SpecimenCollectionItemForm