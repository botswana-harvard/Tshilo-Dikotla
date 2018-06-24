# from django.db.models import get_model

from edc_appointment.models import Appointment
from edc_meta_data.models import CrfMetaDataMixin
# from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_constants.constants import (
    UNSCHEDULED, SCHEDULED, COMPLETED_PROTOCOL_VISIT, DEAD, POS, MALE, MISSED_VISIT)
from edc_export.models import ExportTrackingFieldsMixin
from edc_offstudy.models import OffStudyMixin
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords
from edc_visit_tracking.constants import VISIT_REASON_NO_FOLLOW_UP_CHOICES, LOST_VISIT
from edc_visit_tracking.models import VisitModelMixin

from tshilo_dikotla.choices import VISIT_REASON
from tshilo_dikotla.td_previous_visit_mixin import TdPreviousVisitMixin
from edc_visit_tracking.models.caretaker_fields_mixin import CaretakerFieldsMixin

from .infant_birth import InfantBirth


class InfantVisit(
        CrfMetaDataMixin, SyncModelMixin, TdPreviousVisitMixin, OffStudyMixin, VisitModelMixin,
        CaretakerFieldsMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the infant visits. """

    off_study_model = ('td_infant', 'InfantOffStudy')

    death_report_model = ('td_infant', 'InfantDeathReport')

    consent_model = InfantBirth  # a bit weird, see visit_form_mixin clean()

    history = SyncHistoricalRecords()

    def __str__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    def custom_post_update_crf_meta_data(self):
        """Calls custom methods that manipulate meta data on the post save.

        This method is called in a post-save signal in edc_meta_data."""
        if self.survival_status == DEAD:
            self.require_death_report()
        elif self.reason == COMPLETED_PROTOCOL_VISIT:
            self.require_off_study_report()
        elif self.reason == UNSCHEDULED:
            self.change_to_unscheduled_visit(self.appointment)
        elif self.reason == SCHEDULED:
            pass
#             if self.postnatal_enrollment.enrollment_hiv_status:
#                 self.requires_infant_birth_arv_on_maternal_pos()
#                 self.requires_dna_pcr_on_maternal_pos()
#                 self.requires_circumcision_for_male_at_2030_or_2060()
        return self

#     def requires_infant_birth_arv_on_maternal_pos(self):
#         PostnatalEnrollment = get_model('mb_maternal', 'PostnatalEnrollment')
#         maternal_registered_subject = RegisteredSubject.objects.get(
#             subject_identifier=self.appointment.registered_subject.relative_identifier)
#         postnatal_enrollment = PostnatalEnrollment.objects.get(
#             registered_subject=maternal_registered_subject)
#         if postnatal_enrollment.enrollment_hiv_status == POS:
#             if self.appointment.visit_definition.code == '2000':
#                 self.crf_is_required(self.appointment, 'td_infant', 'infantbirtharv')

#     def requires_dna_pcr_on_maternal_pos(self):
#         PostnatalEnrollment = get_model('td_maternal', 'PostnatalEnrollment')
#         maternal_registered_subject = RegisteredSubject.objects.get(
#             subject_identifier=self.appointment.registered_subject.relative_identifier)
#         postnatal_enrollment = PostnatalEnrollment.objects.get(
#             registered_subject=maternal_registered_subject)
#         if postnatal_enrollment.enrollment_hiv_status == POS:
#             if self.appointment.visit_definition.code in [
#                     '2000', '2010', '2030', '2060', '2090', '2120']:
#                 self.requisition_is_required(
# self.appointment, 'td_lab', 'infantrequisition', 'DNA PCR')

    def requires_circumcision_for_male_at_2030_or_2060(self):
        infant_birth = InfantBirth.objects.get(
            registered_subject=self.appointment.registered_subject)
        if infant_birth.gender == MALE:
            if self.appointment.visit_definition.code == '2030':
                self.crf_is_required(
                    self.appointment, 'td_infant', 'infantcircumcision')
            if self.appointment.visit_definition.code == '2060':
                appointment = Appointment.objects.get(
                    visit_definition__code='2030',
                    registered_subject=self.appointment.registered_subject)
                if appointment:
                    infant_visit = InfantVisit.objects.get(
                        appointment=appointment)
                    if infant_visit.reason == MISSED_VISIT:
                        self.crf_is_required(
                            self.appointment, 'td_infant', 'infantcircumcision')

    def natural_key(self):
        return self.appointment.natural_key()
    natural_key.dependencies = ['edc_appointment.appointment']

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def get_visit_reason_no_follow_up_choices(self):
        """Returns the visit reasons that do not imply any data collection;
        that is, the subject is not available."""
        dct = {}
        for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
            if item not in [COMPLETED_PROTOCOL_VISIT, LOST_VISIT]:
                dct.update({item: item})
        return dct

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Infant Visit"
        verbose_name_plural = "Infant Visit"
