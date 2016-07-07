from django.contrib import admin

from edc_lab.lab_profile.admin import BaseProcessingAdmin

from ..models import AliquotProcessing


class AliquotProcessingAdmin(BaseProcessingAdmin):

    list_display = ('aliquot', 'profile', 'created', 'modified', 'user_created', 'user_modified')

    search_fields = ('aliquot__aliquot_identifier', 'profile__name', 'aliquot__aliquot_type__name',
                     'aliquot__aliquot_type__alpha_code', 'aliquot__aliquot_type__numeric_code')

    list_filter = ('profile', 'created', 'modified', 'user_created', 'user_modified')

admin.site.register(AliquotProcessing, AliquotProcessingAdmin)
