from django.utils import timezone
from dateutil.relativedelta import relativedelta
# from edc_consent.models import ConsentType
from td_registration.models import RegisteredSubject
from edc_constants.constants import (FAILED_ELIGIBILITY, OFF_STUDY, POS, YES,
                                     NO, NOT_APPLICABLE, SCREENED)
from edc_visit_tracking.constants import SCHEDULED

from td_maternal.models import MaternalVisit

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, MaternalOffStudyFactory)


class TestMaternalUltrasound(BaseTestCase):
    """Test eligibility of a mother."""

    def setUp(self):
        super(TestMaternalUltrasound, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

        self.assertEqual(self.maternal_consent.version, '1')
        self.assertEqual(self.registered_subject.subject_identifier, self.maternal_consent.subject_identifier)
        # maternal visit created here.
        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)

    def test_pass_eligibility_on_singleton_pregnancy(self):
        """Test antenatal Enrollment remains as eligible on singleton fetus ultrasound."""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        self.assertEqual(MaternalVisit.objects.all().count(), 1)
        options = {'number_of_gestations': 1,
                   'maternal_visit': maternal_visit,
                   'est_edd_ultrasound': self.antenatal_enrollment.edd_by_lmp + relativedelta(days=17)}
        maternal_ultrasound = MaternalUltraSoundIniFactory(**options)
        self.assertTrue(maternal_ultrasound.antenatal_enrollment.is_eligible)

    def test_fail_eligibility_on_non_singleton_pregnancy(self):
        """Test antenatal Enrollment fails eligible on non-singleton fetus ultrasound."""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        options = {'number_of_gestations': 2,
                   'maternal_visit': maternal_visit}
        maternal_ultrasound = MaternalUltraSoundIniFactory(**options)
        self.assertFalse(maternal_ultrasound.antenatal_enrollment.is_eligible)
        MaternalOffStudyFactory(maternal_visit=maternal_visit)

    def test_create_visit_with_offstudy_on_failure(self):
        """Offstudy visit created on antenatal enrollment failure."""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        options = {'number_of_gestations': 2,
                   'maternal_visit': maternal_visit,
                   'est_edd_ultrasound': self.antenatal_enrollment.edd_by_lmp + relativedelta(days=17)}
        maternal_ultrasound = MaternalUltraSoundIniFactory(**options)
        self.assertFalse(maternal_ultrasound.antenatal_enrollment.is_eligible)
        self.assertEqual(MaternalVisit.objects.filter(
            reason=FAILED_ELIGIBILITY,
            study_status=OFF_STUDY,
            appointment__registered_subject__subject_identifier=self.registered_subject.subject_identifier).count(), 1)

    def test_ga_by_lmp(self):
        """Test GA by LMP correctly calculated considering antenatal enrollment date at lmp and  ultrasound
        date."""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        self.assertEqual(MaternalVisit.objects.all().count(), 1)
        options = {'number_of_gestations': 1,
                   'maternal_visit': maternal_visit,
                   'est_edd_ultrasound': self.antenatal_enrollment.edd_by_lmp + relativedelta(days=17)}
        maternal_ultrasound = MaternalUltraSoundIniFactory(**options)
        enrollment = maternal_ultrasound.antenatal_enrollment
        edd_by_lmp = ((enrollment.last_period_date + relativedelta(years=1) + relativedelta(days=7)) -
            relativedelta(months=3))
        lmp = int(abs(40 - ((enrollment.edd_by_lmp - maternal_ultrasound.report_datetime.date()).days / 7)))
        self.assertEqual(maternal_ultrasound.ga_by_lmp, lmp)

    def test_edd_confirmed(self):
        """Test edd confirmed correctly calculated considering antenatal enrollment date at lmp and  edd from 
        ultrasound."""
        pass

    def test_ga_confirmed(self):
        """Test GA confirmed is correctly calculated considering edd confirmed and the date of the ultra sound."""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        self.assertEqual(MaternalVisit.objects.all().count(), 1)
        options = {'number_of_gestations': 1,
                   'maternal_visit': maternal_visit,
                   'est_edd_ultrasound': self.antenatal_enrollment.edd_by_lmp + relativedelta(days=17)}
        maternal_ultrasound = MaternalUltraSoundIniFactory(**options)
        ga_confirmed = int(abs(40 - ((maternal_ultrasound.edd_confirmed -
            maternal_ultrasound.report_datetime.date()).days / 7)))
        self.assertEqual(maternal_ultrasound.ga_confirmed, ga_confirmed)

    def test_ga_edd_confirmed_with_no_antenatal_lmp(self):
        """Test GA and EDD confirmed are automatically chosen from ultrasound values
        if no LMP at antenatal enrollment"""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        self.assertEqual(MaternalVisit.objects.all().count(), 1)
        options = {'number_of_gestations': 1,
                   'maternal_visit': maternal_visit,
                   'est_edd_ultrasound': timezone.datetime.now().date() + relativedelta(months=5)}
        antenatal = self.antenatal_enrollment
        antenatal.knows_lmp = NO,
        antenatal.last_period_date = None
        antenatal.save()
        maternal_ultrasound = MaternalUltraSoundIniFactory(**options)
        self.assertEqual(maternal_ultrasound.edd_confirmed, maternal_ultrasound.est_edd_ultrasound)

    def test_no_antenatal_lmp_but_eligible_from_ultrasound_gaconfirmed(self):
        """Test if no LMP at antenatal enrollment, can still pass eligibility if 16 < ga > 36 from
        ultrasound initial form"""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        self.assertEqual(MaternalVisit.objects.all().count(), 1)
        options = {'number_of_gestations': 1,
                   'maternal_visit': maternal_visit,
                   'est_edd_ultrasound': timezone.datetime.now().date() + relativedelta(months=5)}
        antenatal = self.antenatal_enrollment
        antenatal.knows_lmp = NO,
        antenatal.last_period_date = None
        antenatal.save()
        ultrasound = MaternalUltraSoundIniFactory(**options)
        antenatal = ultrasound.antenatal_enrollment
        self.assertTrue(antenatal.is_eligible)

    def test_no_antenatal_lmp_but_noteligible_from_ultrasound_gaconfirmed(self):
        """Test if no LMP at antenatal enrollment, can still fail eligibility if 16 < ga > 36 from
        ultrasound initial form"""
        maternal_visit = MaternalVisit.objects.get(appointment__registered_subject=self.registered_subject,
                                                   reason=SCHEDULED,
                                                   appointment__visit_definition__code='1000M')
        self.assertEqual(MaternalVisit.objects.all().count(), 1)
        options = {'number_of_gestations': 1,
                   'maternal_visit': maternal_visit,
                   'est_edd_ultrasound': timezone.datetime.now().date() + relativedelta(months=7)}
        antenatal = self.antenatal_enrollment
        antenatal.knows_lmp = NO,
        antenatal.last_period_date = None
        antenatal.save()
        ultrasound = MaternalUltraSoundIniFactory(**options)
        antenatal = ultrasound.antenatal_enrollment
        self.assertFalse(antenatal.is_eligible)
