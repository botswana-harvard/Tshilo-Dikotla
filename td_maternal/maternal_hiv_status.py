
from td.hiv_result import PostEnrollment, Recent, Test
from td_maternal.models import AntenatalEnrollment, RapidTestResult
from edc_constants.constants import YES


class MaternalHivStatus(PostEnrollment):
    """Returns an instance with the result and result date of the subjects HIV status
    as of reference_datetime.

    Replaces MaternalStatusHelper"""
    def __init__(self, subject_identifier=None, reference_datetime=None, exception_cls=None):
        self.subject_identifier = subject_identifier
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=subject_identifier)
        rapid_test_results = []
        for obj in RapidTestResult.objects.filter(maternal_visit__subject_identifier=subject_identifier):
            rapid_test_results.append(Test(result=obj.result, result_date=obj.result_date))
        super(MaternalHivStatus, self).__init__(
            reference_datetime=reference_datetime,
            exception_cls=exception_cls,
            rapid_results=rapid_test_results,
            enrollment_result=Recent(
                reference_datetime=reference_datetime,
                tested=YES,
                evidence=YES,
                result=antenatal_enrollment.enrollment_hiv_status,
                result_date=antenatal_enrollment.report_datetime.date()))
