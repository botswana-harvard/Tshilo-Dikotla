import pytz
import unittest

from datetime import datetime
from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NEG, NO

from td.hiv_result import EnrollmentResultError
from td.models import Appointment

from ..enrollment_helper import EnrollmentHelper
from ..models import AntenatalEnrollment


class Obj:
    def __init__(self, **kwargs):
        for attr in [field.name for field in AntenatalEnrollment._meta.get_fields()]:
            setattr(self, attr, None)
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.report_datetime = get_utcnow()


class TestResult(unittest.TestCase):

    def test_pos(self):
        """Asserts POS result with evidence is POS."""
        obj = Obj(current_hiv_status=POS, evidence_hiv_status=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, POS)

    def test_result_pos_no_evidence(self):
        """Asserts POS result without evidence requires rapid."""
        obj = Obj(current_hiv_status=POS, evidence_hiv_status=NO)
        self.assertRaises(EnrollmentResultError, EnrollmentHelper, obj)

    def test_result_neg_no_evidence(self):
        """Asserts NEG result with or without evidence is None."""
        obj = Obj(current_hiv_status=NEG, evidence_hiv_status=NO)
        self.assertRaises(EnrollmentResultError, EnrollmentHelper, obj)
        obj = Obj(current_hiv_status=NEG, evidence_hiv_status=YES)
        self.assertRaises(EnrollmentResultError, EnrollmentHelper, obj)

    def test_result_neg_by_week32(self):
        """Asserts NEG result by week 32 test alone requires rapid."""
        obj = Obj(
            week32_test_date=get_utcnow(),
            week32_test=YES,
            week32_result=NEG,
            evidence_32wk_hiv_status=YES)
        self.assertRaises(EnrollmentResultError, EnrollmentHelper, obj)

    def test_result_pos_by_week32_requires_rapid(self):
        """Asserts POS result by week 32 test."""
        obj = Obj(
            week32_test_date=get_utcnow(),
            week32_test=YES,
            week32_result=POS,
            evidence_32wk_hiv_status=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, POS)

    def test_result_neg_by_week32_with_rapid(self):
        """Asserts NEG result by week 32 is NEG if supported by rapid."""
        obj = Obj(
            week32_test_date=get_utcnow(),
            week32_test=YES,
            week32_result=NEG,
            evidence_32wk_hiv_status=YES,
            rapid_test_date=get_utcnow(),
            rapid_test_done=YES,
            rapid_test_result=NEG)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, NEG)

    def test_result_neg_by_rapid(self):
        """Asserts NEG result by rapid test."""
        obj = Obj(
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            rapid_test_date=get_utcnow(),
            rapid_test_done=YES,
            rapid_test_result=NEG)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, NEG)

    def test_result_pos_by_rapid(self):
        """Asserts POS result by rapid test."""
        obj = Obj(
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            rapid_test_date=get_utcnow(),
            rapid_test_done=YES,
            rapid_test_result=POS)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.enrollment_result.result, POS)


class TestGa(unittest.TestCase):

    opts = dict(
        current_hiv_status=POS,
        evidence_hiv_status=YES)

    def test_ga_by_lmp_out_of_range(self):
        """Asserts GA 15, not 16-36, ga_pending will be False."""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=15),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 15)
        self.assertFalse(enrollment_helper.ga_pending)
        self.assertFalse(enrollment_helper.is_eligible)

    def test_ga_by_lmp_in_range_16(self):
        """Asserts GA 16, in 16-36."""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=16),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 16)
        self.assertFalse(enrollment_helper.ga_pending)

    def test_ga_by_lmp_in_range_17(self):
        """Asserts GA 17, in 16-36."""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=17),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 17)
        self.assertFalse(enrollment_helper.ga_pending)

    def test_ga_by_lmp_in_range_36(self):
        """Asserts GA 66, in 16-36."""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=36),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 36)
        self.assertFalse(enrollment_helper.ga_pending)

    def test_ga_absurd(self):
        """Asserts GA none if absurd, ga_pending will be True"""
        obj = Obj(
            last_period_date=get_utcnow() - relativedelta(weeks=40),
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, 40)
        self.assertFalse(enrollment_helper.ga_pending)
        self.assertFalse(enrollment_helper.is_eligible)

    def test_ga_none(self):
        """Asserts GA none if lmp not know."""
        obj = Obj(
            last_period_date=None,
            **self.opts)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertEqual(enrollment_helper.ga.weeks, None)
        self.assertTrue(enrollment_helper.ga_pending)


class TestEdd(TestCase):

    def setUp(self):
        mommy.make_recipe(
            'td_maternal.maternaleligibility',
            report_datetime=pytz.utc.localize(datetime(2016, 10, 8, 9, 15)))
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent',
            consent_datetime=pytz.utc.localize(datetime(2016, 10, 8, 9, 16)))
        self.subject_identifier = maternal_consent.subject_identifier
        self.opts = dict(
            subject_identifier=self.subject_identifier,
            report_datetime=pytz.utc.localize(datetime(2016, 10, 15)),
            current_hiv_status=POS,
            evidence_hiv_status=YES,
        )

    def test_edd_is_from_lmp(self):
        """Asserts GA none if lmp not know."""
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment',
            last_period_date=datetime(2016, 10, 15) - relativedelta(weeks=22),
            **self.opts)
        self.assertEqual(antenatal_enrollment.edd_by_lmp, datetime(2017, 2, 18))
        self.assertEqual(antenatal_enrollment.ga_weeks, 18)
        self.assertFalse(antenatal_enrollment.ga_pending)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_edd_ultrasound(self):
        """Asserts EDD from ultrasound is used."""
        mommy.make_recipe(
            'td_maternal.maternalconsent',
            consent_datetime=pytz.utc.localize(datetime(2016, 10, 8, 9, 15)))
        antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment',
            **self.opts)
        self.assertTrue(antenatal_enrollment.is_eligible)
        self.assertEqual(Appointment.objects.all().count(), 1)
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code='1000M')
        maternal_visit = mommy.make_recipe(
            'td_maternal.maternalvisit',
            appointment=appointment)
        ultrasound_obj = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            report_datetime=datetime(2016, 10, 11),
            maternal_visit=maternal_visit,
            est_edd_ultrasound=datetime(2016, 10, 11),
            ga_by_ultrasound_wks=17)
        antenatal_enrollment.save()
        self.assertEqual(antenatal_enrollment.edd_by_lmp, datetime(2017, 2, 7))  # not by LMP!
        self.assertEqual(antenatal_enrollment.ga_weeks, 17)
        self.assertFalse(antenatal_enrollment.ga_pending)
        self.assertTrue(antenatal_enrollment.is_eligible)
