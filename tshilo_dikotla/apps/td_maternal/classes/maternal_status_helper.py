from django.db.models import Q
from dateutil.relativedelta import relativedelta

from edc_registration.models import RegisteredSubject
from edc_constants.constants import POS, NEG, UNK

from tshilo_dikotla.apps.td_maternal.models import AntenatalEnrollment, RapidTestResult
from django.core.exceptions import ValidationError


class MaternalStatusHelper(object):

    def __init__(self, maternal_visit):
        self.maternal_visit = maternal_visit

    @property
    def hiv_status(self):
        if not self.maternal_visit:
            return ''
        for visit in self.previous_visits:
            rapid_test_result = None
            try:
                rapid_test_result = RapidTestResult.objects.get(maternal_visit=visit)
                status = self._evaluate_status_from_rapid_tests(visit,
                                                                (rapid_test_result, 'result', 'result_date'))
                if status in [POS, NEG, UNK]:
                    return status
                elif status is None:
                    # Keep trying more past visits
                    continue
                else:
                    raise ValidationError('Unexpected Maternal Status condition in MaternalStatusHelper. Got {}'.format(
                        status))
            except RapidTestResult.DoesNotExist:
                pass
        # If we have exhausted all visits without a concrete status then use enrollment status.
        antenatal_enrollment = AntenatalEnrollment.objects.get(
            registered_subject=self.maternal_visit.appointment.registered_subject)
        status = self._evaluate_status_from_rapid_tests(
            visit, (antenatal_enrollment, 'enrollment_hiv_status', 'rapid_test_date'))
        if status in [POS, NEG, UNK]:
                return status
        elif status is None:
            raise ValidationError('Unexpected Maternal Status condition in MaternalStatusHelper. Got {}'.format(
                status))
        return status

    @property
    def enrollment_hiv_status(self):
        if not self.maternal_visit:
            return ''
        else:
            return AntenatalEnrollment.objects.get(
                registered_subject=self.maternal_visit.appointment.registered_subject).enrollment_hiv_status

    @property
    def eligible_for_cd4(self, ):
#         latest_interim_idcc = None
#         latest_cd4_requisition = None
#         latest_visit = self.previous_visits.first()
#         try:
#             latest_interim_idcc = MaternalInterimIdcc.objects.get(maternal_visit=latest_visit)
#         except MaternalInterimIdcc.DoesNotExist:
#             pass
#         try:
#             latest_cd4_requisition = MaternalRequisition.objects.get(maternal_visit=latest_visit)
#         except MaternalRequisition.DoesNotExist:
#             pass
#         
#         if self.hiv_status == POS and
        return True

    @property
    def previous_visits(self):
        if not self.maternal_visit:
            visits = []
        else:
            visits = self.maternal_visit.__class__.objects.filter(
                appointment__registered_subject=self.maternal_visit.appointment.registered_subject).order_by(
                '-appointment__visit_definition__time_point')
        return visits

    def _evaluate_status_from_rapid_tests(self, maternal_visit, intance_result_date_tuple):
        if intance_result_date_tuple[0]:
            if getattr(intance_result_date_tuple[0], intance_result_date_tuple[1]) == POS:
                return POS
            elif (getattr(intance_result_date_tuple[0], intance_result_date_tuple[1]) == NEG and
                  getattr(intance_result_date_tuple[0], intance_result_date_tuple[2]) and
                  getattr(intance_result_date_tuple[0], intance_result_date_tuple[2]) >
                  (self.maternal_visit.report_datetime.date() - relativedelta(months=3))):
                return NEG
            else:
                return UNK
        else:
            return None
