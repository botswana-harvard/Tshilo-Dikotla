import os
import pytz

from datetime import time, datetime
from dateutil.relativedelta import relativedelta
from model_mommy import mommy
from unipath import Path

from edc_base.test_mixins import AddVisitMixin, ReferenceDateMixin, CompleteCrfsMixin, TestMixinError
from edc_constants.constants import NEG, YES, NO, UNKNOWN

from td_list.models import RandomizationItem


RAPID = 'rapid'
RECENT = 'recent'
ENROLLMENT = 'enrollment'


def load_test_randomization():
    """Loads a test randomization CSV and adds data to RandomizationItem model."""
    f = open(os.path.join(
             Path(os.path.dirname(os.path.realpath(__file__))), 'test_randomization.csv'))
    for index, line in enumerate(f.readlines()):
        if index == 0:
            continue
        seq, drug_assignment = line.split(',')
        RandomizationItem.objects.get_or_create(name=seq, field_name=drug_assignment)


class AddMaternalVisitMixin(AddVisitMixin):

    maternal_model_label = 'td_maternal.maternalvisit'

    def add_maternal_visit(self, visit_code, reason=None):
        return self.add_visit(self.maternal_model_label, visit_code, reason)

    def add_maternal_visits(self, *visit_codes):
        return self.add_visits(self.maternal_model_label, *visit_codes)

    def get_maternal_visit(self, visit_code):
        return self.get_visit(self.maternal_model_label, visit_code)

    def get_last_maternal_visit(self):
        return self.get_last_visit(self.maternal_model_label)


class CompleteMaternalCrfsMixin(CompleteCrfsMixin):

    def mommy_options(self, report_datetime):
        return {
            'td_maternal.maternalultrasoundinitial': dict(
                est_edd_ultrasound=report_datetime + relativedelta(weeks=20),
                ga_by_ultrasound_wks=20)
        }

    def complete_required_crfs(self, *visit_codes):
        """Complete all required CRFs for a visit(s) using mommy defaults."""
        for visit_code in visit_codes:
            maternal_visit = self.add_maternal_visit(visit_code)
            super(CompleteMaternalCrfsMixin, self).complete_required_crfs(
                visit_code, maternal_visit, 'maternal_visit')


class MaternalTestMixin(CompleteMaternalCrfsMixin, AddMaternalVisitMixin):
    pass


class MotherMixin(ReferenceDateMixin, MaternalTestMixin):
    """Creates a POS mother."""
    def setUp(self):
        super(MotherMixin, self).setUp()
        load_test_randomization()
        self.study_site = '40'
        self.maternal_eligibility = self.make_eligibility()
        self.maternal_consent = self.make_consent()
        self.subject_identifier = self.maternal_consent.subject_identifier

    def make_eligibility(self):
        return mommy.make_recipe('td_maternal.maternaleligibility')

    def make_consent(self):
        return mommy.make_recipe(
            'td_maternal.maternalconsent',
            consent_datetime=self.mixin_reference_datetime,
            maternal_eligibility_reference=self.maternal_eligibility.reference,)

    def make_positive_mother(self):
        """Make a POS mother LMP 25wks with POS result with evidence (no recent or rapid test)."""
        self.antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment_pos',
            report_datetime=self.mixin_reference_datetime,
            last_period_date=(self.mixin_reference_datetime - relativedelta(weeks=25)).date(),
            rapid_test_done=None,
            rapid_test_result=None,
            week32_test_date=None,
            subject_identifier=self.subject_identifier)
        if self.antenatal_enrollment.reasons_not_eligible:
            self.assertIsNone(self.antenatal_enrollment.reasons_not_eligible)
        self.assertTrue(self.antenatal_enrollment.is_eligible)

    def make_negative_mother(self, use_result=None):
        """Make a NEG mother LMP 25wks with NEG by current, recent or rapid."""
        use_result = use_result or RAPID
        if use_result == ENROLLMENT:
            options = dict(
                current_hiv_status=NEG,  # never valid
                evidence_hiv_status=YES,
                week32_test=NO,
                week32_test_date=None,
                week32_result=None,
                evidence_32wk_hiv_status=None,
                rapid_test_done=NO,
                rapid_test_date=None,
                rapid_test_result=None)
        elif use_result == RECENT:  # a.k.a week32, e.g. a recent test some time after 32wks GA
            options = dict(
                current_hiv_status=UNKNOWN,
                evidence_hiv_status=NO,
                week32_test=YES,
                week32_test_date=(self.mixin_reference_datetime - relativedelta(weeks=4)).date(),
                week32_result=NEG,
                evidence_32wk_hiv_status=YES,
                rapid_test_done=NO,
                rapid_test_date=None,
                rapid_test_result=None)
        elif use_result == RAPID:
            options = dict(
                current_hiv_status=UNKNOWN,
                evidence_hiv_status=NO,
                week32_test=NO,
                week32_test_date=None,
                week32_result=None,
                evidence_32wk_hiv_status=None,
                rapid_test_done=YES,
                rapid_test_date=(self.mixin_reference_datetime - relativedelta(weeks=4)).date(),
                rapid_test_result=NEG)
        self.antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment_neg',
            report_datetime=self.mixin_reference_datetime,
            last_period_date=(self.mixin_reference_datetime - relativedelta(weeks=25)).date(),
            subject_identifier=self.subject_identifier,
            **options)
        if self.antenatal_enrollment.reasons_not_eligible:
            raise TestMixinError(self.antenatal_enrollment.reasons_not_eligible)
        self.assertTrue(self.antenatal_enrollment.is_eligible)

    def make_antenatal_enrollment_two(self, report_datetime=None):
        """Complete ANC 2 on given report_datetime."""
        report_datetime = report_datetime or self.get_maternal_visit('1000M').report_datetime + relativedelta(months=1)
        self.antenatal_enrollment_two = mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo',
            report_datetime=report_datetime,
            subject_identifier=self.subject_identifier)

    def make_delivery(self, report_datetime=None, **options):
        """Deliver one live infant on given report_datetime."""
        report_datetime = report_datetime or pytz.utc.localize(
            datetime.combine(self.antenatal_enrollment.edd, time()))
        live_infants = options.get('live_infants', 1)
        options.update(live_infants=live_infants)
        self.maternal_lab_del = mommy.make_recipe(
            'td_maternal.maternallabdel',
            report_datetime=report_datetime,
            subject_identifier=self.subject_identifier,
            **options)

    def make_rapid_test(self, result, result_date=None, visit=None):
        """Makes a rapid test with the given result.

        If no visit use last visit, if no result date use visit report_datetime."""
        visit = visit or self.get_last_maternal_visit()
        return mommy.make_recipe(
            'td_maternal.rapidtestresult',
            maternal_visit=visit,
            result=result,
            result_date=result_date or visit.report_datetime.date())


class PosMotherMixin(MotherMixin):
    """Creates an eligible POS mother."""
    def setUp(self):
        super(PosMotherMixin, self).setUp()
        self.make_positive_mother()


class NegMotherMixin(MotherMixin):
    """Creates an eligible NEG mother."""
    def setUp(self):
        super(NegMotherMixin, self).setUp()
        self.make_negative_mother(use_result=RAPID)
