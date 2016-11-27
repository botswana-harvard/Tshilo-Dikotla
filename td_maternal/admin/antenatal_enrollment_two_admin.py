from django.contrib import admin
from collections import OrderedDict

from edc_registration.models import RegisteredSubject
from edc_export.actions import export_as_csv_action

from td.admin_mixins import ModelAdminMixin

from ..forms import AntenatalEnrollmentTwoForm
from ..models import AntenatalEnrollmentTwo
from edc_base.modeladmin_mixins import ModelAdminNextUrlRedirectMixin


@admin.register(AntenatalEnrollmentTwo)
class AntenatalEnrollmentTwoAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    dashboard_type = 'maternal'
    form = AntenatalEnrollmentTwoForm

    radio_fields = {'antenatal_visits': admin.VERTICAL}

    list_display = ('subject_identifier', 'report_datetime', 'antenatal_visits')

    actions = [
        export_as_csv_action(
            description="CSV Export of Antenatal Enrollment",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 'registered': 'registered_subject__registration_datetime'}),
        )]
