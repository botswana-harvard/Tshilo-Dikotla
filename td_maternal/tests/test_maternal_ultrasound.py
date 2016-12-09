from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from edc_constants.constants import NO
from edc_pregnancy_utils.constants import ULTRASOUND

from ..models import AntenatalEnrollment, MaternalOffstudy

from .mixins import AddVisitMotherMixin, PosMotherMixin
from edc_pregnancy_utils.lmp import Lmp


class TestMaternalUltrasound(AddVisitMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalUltrasound, self).setUp()
        self.add_maternal_visit('1000M')

    def test_pass_eligibility_on_singleton_pregnancy(self):
        """Test antenatal Enrollment remains as eligible on singleton fetus ultrasound."""
        maternal_visit = self.get_maternal_visit('1000M')
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            est_edd_ultrasound=timezone.now().date() + relativedelta(weeks=20),
            ga_by_ultrasound_wks=20,
            ga_by_ultrasound_days=4)
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_fail_eligibility_on_non_singleton_pregnancy(self):
        """Test antenatal Enrollment fails eligible on non-singleton fetus ultrasound."""
        maternal_visit = self.get_maternal_visit('1000M')
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            number_of_gestations=2,
            maternal_visit=maternal_visit,
            est_edd_ultrasound=timezone.now().date() + relativedelta(weeks=20),
            ga_by_ultrasound_wks=20,
            ga_by_ultrasound_days=4)
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_ineligible_adds_offstudy(self):
        """Offstudy created on antenatal enrollment failure."""
        maternal_visit = self.get_maternal_visit('1000M')
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        antenatal_enrollment.knows_lmp = NO,
        antenatal_enrollment.last_period_date = None
        antenatal_enrollment.unenrolled = None
        antenatal_enrollment.save()
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            est_edd_ultrasound=timezone.now().date() + relativedelta(weeks=3),
            ga_by_ultrasound_wks=37,
            ga_by_ultrasound_days=4)
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertFalse(antenatal_enrollment.is_eligible)
        try:
            MaternalOffstudy.objects.get(subject_identifier=self.subject_identifier)
        except MaternalOffstudy.DoesNotExist:
            self.fail('MaternalOffstudy.DoesNotExist unexpectedly raised')

    def test_ga_by_lmp(self):
        """Test GA by LMP correctly calculated considering antenatal enrollment date at lmp and  ultrasound
        date."""
        maternal_visit = self.get_maternal_visit('1000M')
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            est_edd_ultrasound=antenatal_enrollment.edd_by_lmp + relativedelta(days=17),
            ga_by_ultrasound_wks=22,
            ga_by_ultrasound_days=3)
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        lmp = Lmp(
            lmp=antenatal_enrollment.last_period_date,
            reference_date=maternal_ultrasound.report_datetime.date())
        self.assertEqual(maternal_ultrasound.ga_by_lmp, lmp.ga.weeks)

# TODO: currrent Ultrasound() requires GA weeks, GA days and EDD from the Ultrasound report.
#     def test_ga_confirmed(self):
#         """Test GA confirmed is correctly calculated considering edd confirmed and the date of the ultra sound."""
#         maternal_visit = self.get_maternal_visit('1000M')
#         antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
#         antenatal_enrollment.last_period_date = (timezone.now() - relativedelta(weeks=25)).date()
#         antenatal_enrollment.save()
#         antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
#         maternal_ultrasound = mommy.make_recipe(
#             'td_maternal.maternalultrasoundinitial',
#             maternal_visit=maternal_visit,
#             report_datetime=maternal_visit.report_datetime,
#             ga_by_ultrasound_wks=2,
#             ga_by_ultrasound_days=4,
#             est_edd_ultrasound=antenatal_enrollment.edd_by_lmp + relativedelta(days=17))
#         ga_confirmed = int(
#             abs(40 - ((maternal_ultrasound.edd_confirmed - maternal_ultrasound.report_datetime.date()).days / 7)))
#         antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
#         self.assertEqual(maternal_ultrasound.ga_confirmed, ga_confirmed)
#         self.assertEqual(maternal_ultrasound.ga_confirmed, antenatal_enrollment.enrollment_ga)
#         self.assertEqual(antenatal_enrollment.enrollment_ga_method, ULTRASOUND)

    def test_ga_edd_confirmed_with_no_antenatal_lmp(self):
        """Test GA and EDD confirmed are automatically chosen from ultrasound values
        if no LMP at antenatal enrollment"""
        maternal_visit = self.get_maternal_visit('1000M')
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        antenatal_enrollment.knows_lmp = NO,
        antenatal_enrollment.last_period_date = None
        antenatal_enrollment.save()
        maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            report_datetime=maternal_visit.report_datetime,
            est_edd_ultrasound=(maternal_visit.report_datetime + relativedelta(weeks=20)).date(),
            ga_by_ultrasound_wks=20,
            ga_by_ultrasound_days=4)
        self.assertEqual(maternal_ultrasound.edd_confirmed.date(), maternal_ultrasound.est_edd_ultrasound)
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertEqual(antenatal_enrollment.edd, maternal_ultrasound.edd_confirmed.date())
        self.assertEqual(antenatal_enrollment.edd_method, str(ULTRASOUND))

    def test_no_lmp_with_ultrasound_gaconfirmed_eligible(self):
        """Test if no LMP at antenatal enrollment, can still pass or fail eligibility based on ultrasound GA."""
        maternal_visit = self.get_maternal_visit('1000M')
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertTrue(antenatal_enrollment.is_eligible)
        antenatal_enrollment.knows_lmp = NO,
        antenatal_enrollment.last_period_date = None
        antenatal_enrollment.unenrolled = None
        antenatal_enrollment.save()
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            est_edd_ultrasound=(timezone.now() + relativedelta(weeks=20)).date(),
            ga_by_ultrasound_wks=20,
            ga_by_ultrasound_days=4)
        self.assertIsNone(ultrasound.ga_by_lmp)
        self.assertEqual(ultrasound.ga_by_ultrasound_wks, 20)
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_no_lmp_with_ultrasound_gaconfirmed_ineligible16(self):
        """Test if no LMP at antenatal enrollment, can still pass or fail eligibility based on ultrasound GA."""
        maternal_visit = self.get_maternal_visit('1000M')
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertTrue(antenatal_enrollment.is_eligible)
        antenatal_enrollment.knows_lmp = NO,
        antenatal_enrollment.last_period_date = None
        antenatal_enrollment.unenrolled = None
        antenatal_enrollment.save()
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            est_edd_ultrasound=timezone.now().date() + relativedelta(weeks=24),
            ga_by_ultrasound_wks=16,
            ga_by_ultrasound_days=4)
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_no_lmp_with_ultrasound_gaconfirmed_eligible36(self):
        """Test if no LMP at antenatal enrollment, can still pass or fail eligibility based on ultrasound GA."""
        maternal_visit = self.get_maternal_visit('1000M')
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertTrue(antenatal_enrollment.is_eligible)
        antenatal_enrollment.knows_lmp = NO,
        antenatal_enrollment.last_period_date = None
        antenatal_enrollment.unenrolled = None
        antenatal_enrollment.save()
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            est_edd_ultrasound=timezone.now().date() + relativedelta(weeks=4),
            ga_by_ultrasound_wks=36,
            ga_by_ultrasound_days=4)
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_no_lmp_with_ultrasound_gaconfirmed_ineligible37(self):
        """Test if no LMP at antenatal enrollment, can still pass or fail eligibility based on ultrasound GA."""
        maternal_visit = self.get_maternal_visit('1000M')
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertTrue(antenatal_enrollment.is_eligible)
        antenatal_enrollment.knows_lmp = NO,
        antenatal_enrollment.last_period_date = None
        antenatal_enrollment.unenrolled = None
        antenatal_enrollment.save()
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            est_edd_ultrasound=timezone.now().date() + relativedelta(weeks=3),
            ga_by_ultrasound_wks=37,
            ga_by_ultrasound_days=4)
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
        self.assertFalse(antenatal_enrollment.is_eligible)
