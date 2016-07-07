from edc_constants.constants import (
    FAILED_ELIGIBILITY, UNSCHEDULED, COMPLETED_PROTOCOL_VISIT, NEG, POS, OFF_STUDY)
from edc_meta_data.models import CrfMetaDataMixin


class MaternalVisitCrfMetaDataMixin(CrfMetaDataMixin):

    def custom_post_update_crf_meta_data(self):
        """Custom methods that manipulate meta data on the post save.

        This method is called in the edc_meta_data signal."""
#         if self.reason == FAILED_ELIGIBILITY:
#             self.study_status = OFF_STUDY
#         elif self.reason == UNSCHEDULED:
#             self.change_to_unscheduled_visit(self.appointment)
#         elif self.reason == COMPLETED_PROTOCOL_VISIT:
#             self.study_status = OFF_STUDY
#         else:
#             self.required_for_maternal_pos()
#             self.required_for_maternal_not_pos()
#             self.required_labs_for_maternal_neg()
#             self.required_forms_for_maternal_neg()
        pass
        return self

    def required_forms_for_maternal_neg(self):
        """If attempt to change an offstudy to scheduled visit has been successful, ensure that
        necessary forms at 1000M are REQUIRED"""
        if self.enrollment_hiv_status == NEG or self.scheduled_rapid_test == NEG:
            if self.appointment.visit_definition.code == '1000M':
                model_names = [
                    'maternallocator', 'maternaldemographics', 'maternalmedicalhistory',
                    'maternalobstericalhistory']
                for model_name in model_names:
                    self.crf_is_required(self.appointment, 'td_maternal', model_name)
                self.crf_is_not_required(self.appointment, 'td_maternal', 'maternaloffstudy')

    def required_for_maternal_pos(self):
        if self.enrollment_hiv_status == POS or self.scheduled_rapid_test == POS:
            if self.appointment.visit_definition.code == '1000M':
                model_names = ['maternalclinicalhistory', 'maternalarvhistory', 'maternalarvpreg']
                for model_name in model_names:
                    self.crf_is_required(self.appointment, 'td_maternal', model_name)
            elif self.appointment.visit_definition.code == '2000M':
                model_names = ['maternalarvpreg', 'maternallabdelclinic']
                for model_name in model_names:
                    self.crf_is_required(self.appointment, 'td_maternal', model_name)
                    for labs in ['Viral Load', 'Breast Milk (Storage)', 'Vaginal swab (Storage)',
                                 'Rectal swab (Storage)', 'Skin Swab (Storage)',
                                 'Vaginal STI Swab (Storage)', 'CD4/ CD8']:
                        self.requisition_is_required(self.appointment, 'td_lab', 'maternalrequisition', labs)
            elif self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                model_names = ['maternalarvpost', 'maternalarvpostadh']
                for model_name in model_names:
                    self.crf_is_required(self.appointment, 'td_maternal', model_name)
                self.requisition_is_required(self.appointment, 'td_lab', 'maternalrequisition', 'Viral Load')
            if self.appointment.visit_definition.code == '2010M':
                self.requisition_is_required(
                    self.appointment, 'td_lab', 'maternalrequisition', 'Breast Milk (Storage)')

    def required_for_maternal_not_pos(self):
        if self.enrollment_hiv_status == NEG and self.scheduled_rapid_test != POS:
            if self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                self.crf_is_required(self.appointment, 'td_maternal', 'rapidtestresult')

    def required_labs_for_maternal_neg(self):
        if self.enrollment_hiv_status == NEG and self.scheduled_rapid_test != POS:
            if self.appointment.visit_definition.code == '2000M':
                for labs in ['Breast Milk (Storage)', 'Vaginal swab (Storage)',
                             'Rectal swab (Storage)', 'Skin Swab (Storage)',
                             'Vaginal STI Swab (Storage)', 'CD4/ CD8']:
                    self.requisition_is_required(self.appointment, 'td_lab', 'maternalrequisition', labs)
            if self.appointment.visit_definition.code == '2010M':
                self.requisition_is_required(
                    self.appointment, 'td_lab', 'maternalrequisition', 'Breast Milk (Storage)')

    class Meta:
        abstract = True
