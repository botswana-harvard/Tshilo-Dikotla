from collections import OrderedDict

from edc_export.actions import export_as_csv_action

from tshilo_dikotla.admin_mixins import EdcBaseModelAdminMixin
from ..models import MaternalVisit
# from django.urls.base import reverse
from edc_base.modeladmin.mixins import ModelAdminNextUrlRedirectMixin


class BaseMaternalModelAdmin(EdcBaseModelAdminMixin, ModelAdminNextUrlRedirectMixin):

    dashboard_type = 'maternal'
    visit_model_name = 'maternalvisit'

    def redirect_url(self, request, obj, post_url_continue=None):
        return request.GET.get('next')

#     def redirect_url(self, request, obj, post_url_continue=None):
#         args = request.GET.dict()
#         args.pop('visit_code')
#         url_name = request.GET.get(self.querystring_name)
#         subject_identifier = request.GET.get('subject_identifier')
#         appointment_id = request.GET.get('appointment_pk')
#         dashboard_url = reverse(url_name, kwargs={'appointment_pk': appointment_id, 'subject_identifier': subject_identifier})
#         show = 'show={}'.format(request.GET.get('show', None))
#         next_url = "{}?{}".format(dashboard_url, show)
#         return next_url

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('subject_identifier'):
                kwargs["queryset"] = MaternalVisit.objects.filter(
                    appointment__subject_identifier=request.GET.get('subject_identifier'),
                    appointment__visit_code=request.GET.get('visit_code'))
        return super(BaseMaternalModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    actions = [
        export_as_csv_action(
            description="Export to CSV file",
            fields=[],
            delimiter=',',
            exclude=['maternal_visit', 'user_created', 'user_modified', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_visit__appointment__registered_subject__dob',
                 'screened': 'maternal_visit__appointment__registered_subject__screening_datetime',
                 'registered': 'maternal_visit__appointment__registered_subject__registration_datetime',
                 'visit_code': 'maternal_visit__appointment__visit_definition__code',
                 'visit_reason': 'maternal_visit__reason',
                 'visit_study_status': 'maternal_visit__study_status'}),
        )]
