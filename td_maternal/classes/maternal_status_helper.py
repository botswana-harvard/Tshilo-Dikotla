from django.db.models import Q
from dateutil.relativedelta import relativedelta

from td_registration.models import RegisteredSubject
from edc_constants.constants import POS, NEG, UNK, IND

from td_maternal.models import AntenatalEnrollment, RapidTestResult, MaternalInterimIdcc
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
                if status in [POS, NEG, UNK, IND]:
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
            registered_subject__subject_identifier=self.maternal_visit.appointment.subject_identifier)
        status = self._evaluate_status_from_rapid_tests(
            visit, (antenatal_enrollment, 'enrollment_hiv_status', 'rapid_test_date'))
        if status == UNK:
            # Check that the week32_test_date is still within 3 months
            status = self._evaluate_status_from_rapid_tests(
                visit, (antenatal_enrollment, 'enrollment_hiv_status', 'week32_test_date'))
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
                registered_subject__subject_identifier=self.maternal_visit.appointment.subject_identifier).enrollment_hiv_status

    @property
    def eligible_for_cd4(self):
        latest_interim_idcc = None
        try:
            latest_interim_idcc = MaternalInterimIdcc.objects.get(maternal_visit=self.maternal_visit)
            if latest_interim_idcc.recent_cd4_date:
                if ((self.maternal_visit.report_datetime.date() - relativedelta(months=3)) > latest_interim_idcc.recent_cd4_date) and self.hiv_status == POS:
                    return True
                else:
                    return False
        except MaternalInterimIdcc.DoesNotExist:
            pass
        return True

    @property
    def previous_visits(self):
        if not self.maternal_visit:
            visits = []
        else:
            visits = self.maternal_visit.__class__.objects.filter(
                appointment__subject_identifier=self.maternal_visit.appointment.subject_identifier).order_by(
                '-appointment__visit_code_sequence')
        return visits

    def _evaluate_status_from_rapid_tests(self, maternal_visit, intance_result_date_tuple):
        if intance_result_date_tuple[0]:
            if getattr(intance_result_date_tuple[0], intance_result_date_tuple[1]) == POS:
                return POS
            if getattr(intance_result_date_tuple[0], intance_result_date_tuple[1]) == IND:
                return IND
            elif (getattr(intance_result_date_tuple[0], intance_result_date_tuple[1]) == NEG and
                  getattr(intance_result_date_tuple[0], intance_result_date_tuple[2]) and
                  getattr(intance_result_date_tuple[0], intance_result_date_tuple[2]) >
                  (self.maternal_visit.report_datetime.date() - relativedelta(months=3))):
                return NEG
            else:
                return UNK
        else:
            return None
