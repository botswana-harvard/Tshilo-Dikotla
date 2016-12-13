from edc_visit_tracking.modeladmin_mixins import CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin

from td.admin_mixins import ModelAdminMixin


class CrfModelAdminMixin(VisitTrackingCrfModelAdminMixin, ModelAdminMixin):

    visit_model = 'td_infant.infantvisit'
    visit_attr = 'infant_visit'

    instructions = (
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')
