# from edc_lab.lab_clinic_api.classes import EdcLabResults


class DashboardMixin(object):

#     def render_labs(self):
#         if self._requisition_model:
#             edc_lab_results = EdcLabResults()
#             return edc_lab_results.results_template(self.subject_identifier, False)
#         return ''

    def get_context_data(self, **kwargs):
        self.context = super(DashboardMixin, self).get_context_data(**kwargs)
        self.context.update(scheduled_lab_bucket=True)
        return self.context
