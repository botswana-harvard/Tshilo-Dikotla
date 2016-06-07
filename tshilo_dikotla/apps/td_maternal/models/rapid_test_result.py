from django.db import models

# from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO, POS_NEG

from .maternal_crf_model import MaternalCrfModel


class RapidTestResult(MaternalCrfModel):

    """ A model completed by the user on the mother's rapid test result. """

    rapid_test_done = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO,
        max_length=3)

    result_date = models.DateField(
        verbose_name="Date of rapid test",
        null=True,
        blank=True)

    result = models.CharField(
        verbose_name="What is the rapid test result?",
        choices=POS_NEG,
        null=True,
        blank=True,
        max_length=15)

    comments = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        null=True)

#     history = AuditTrail()

    def get_result_datetime(self):
        return self.report_datetime

    def get_test_code(self):
        return 'HIV'

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Rapid Test Result'
        verbose_name_plural = 'Rapid Test Result'
