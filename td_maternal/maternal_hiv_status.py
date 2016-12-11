from edc_constants.constants import YES

from td.hiv_result import PostEnrollmentResult, Recent, Rapid, PostEnrollmentResultError
from td_maternal.models import AntenatalEnrollment, RapidTestResult


class MaternalHivStatus(PostEnrollmentResult):
    """A class with the result and result date of the subjects HIV status
    as of reference_datetime.

    If not results are valid either returns None or raises an exception.

    # TODO: merge this class with PostEnrollmentResult??"""
    def __init__(self, subject_identifier=None, reference_datetime=None):
        try:
            options = dict(
                reference_datetime=reference_datetime,
                rapid_results=self.get_rapid_results(reference_datetime, subject_identifier),
                enrollment_result=self.get_enrollment_result(reference_datetime, subject_identifier))
        except AntenatalEnrollment.DoesNotExist:
            raise PostEnrollmentResultError(
                'Antenatal Enrollment is required to assess HIV status post-enrollment')
        super(MaternalHivStatus, self).__init__(**options)

    def get_enrollment_result(self, reference_datetime, subject_identifier):
        """Returns the enrollment result wrapped in the Recent result class."""
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=subject_identifier)
        return Recent(
            reference_datetime=reference_datetime,
            tested=YES,
            evidence=YES,
            result=antenatal_enrollment.enrollment_hiv_status,
            result_date=antenatal_enrollment.report_datetime.date())

    def get_rapid_results(self, reference_datetime, subject_identifier):
        """Returns a list of rapid test results wrapped in the Rapid result class."""
        rapid_test_results = []
        for obj in RapidTestResult.objects.filter(
                maternal_visit__subject_identifier=subject_identifier,
                result_date__lte=reference_datetime.date()):
            rapid_test_results.append(
                Rapid(reference_datetime=reference_datetime, result=obj.result, result_date=obj.result_date))
        return rapid_test_results
