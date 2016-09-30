from django.contrib import admin

from td_registration.models import RegisteredSubject
from edc_registration.admin import RegisteredSubjectModelAdminMixin


@admin.register(RegisteredSubject)
class RegisteredSubjectAdmin(RegisteredSubjectModelAdminMixin, admin.ModelAdmin):
    pass
