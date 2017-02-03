from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_constants.constants import SCHEDULED, POS, YES, NO, NOT_APPLICABLE
from edc_appointment.models import Appointment

from td_maternal.models import MaternalVisit

from td_maternal.tests import BaseTestCase
from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabourDelFactory,
                                         MaternalVisitFactory)
from td_infant.forms import InfantNvpAdjustmentForm
from .factories import InfantBirthFactory, InfantVisitFactory, InfantNvpDispensingFactory


class TestInfantNvpAdjustmentForm(BaseTestCase):

    def setUp(self):
        super(TestInfantNvpAdjustmentForm, self).setUp()
        maternal_eligibility = MaternalEligibilityFactory()
        MaternalConsentFactory(
            maternal_eligibility=maternal_eligibility)
        registered_subject = maternal_eligibility.registered_subject

        options = {'registered_subject': registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}

        antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(antenatal_enrollment.is_eligible)
        maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        MaternalUltraSoundIniFactory(
            maternal_visit=maternal_visit, number_of_gestations=1,)
        AntenatalVisitMembershipFactory(registered_subject=registered_subject)
        maternal_labour_del = MaternalLabourDelFactory(registered_subject=registered_subject,
                                                       live_infants_to_register=1)
        MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=registered_subject.subject_identifier,
            subject_type='infant')
        InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=maternal_labour_del)
        appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        infant_visit = InfantVisitFactory(appointment=appointment)
        InfantNvpDispensingFactory(infant_visit=infant_visit, nvp_prophylaxis=YES)
        appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        infant_visit = InfantVisitFactory(appointment=appointment)
        self.options = {
            'infant_visit': infant_visit.id,
            'report_datetime': timezone.now().date(),
            'dose_adjustment': NO,
            'adjusted_dose': None,
            'dose_4_weeks': YES,
            'incomplete_dose': None,
        }

    def test_validate_dose_adjustment_yes_adjusted_dose_no(self):
        self.options.update(dose_adjustment=YES, adjusted_dose=None)
        form = InfantNvpAdjustmentForm(data=self.options)
        self.assertIn(
            u'If there was a dose adjustment, please give the adjusted dose.',
            form.errors.get('__all__'))

    def test_validate_dose_adjustment_no_adjusted_dose_not_none(self):
        self.options.update(dose_adjustment=NO, adjusted_dose='20')
        form = InfantNvpAdjustmentForm(data=self.options)
        self.assertIn(
            u'Infant\'s dose was not adjusted, please do not give an adjust dose.',
            form.errors.get('__all__'))

    def test_validate_dose_4_weeks_yes_incomplete_dose_none(self):
        self.options.update(dose_4_weeks=YES, incomplete_dose='20')
        form = InfantNvpAdjustmentForm(data=self.options)
        self.assertIn(
            u'Medication was taken daily for 4 weeks, don\'t give reason for incomplete dose.',
            form.errors.get('__all__'))

    def test_validate_dose_4_weeks_not_incomplete_dose_not_none(self):
        self.options.update(dose_4_weeks=NO, incomplete_dose=None)
        form = InfantNvpAdjustmentForm(data=self.options)
        self.assertIn(
            u'Medication was not taken daily for 4 weeks, please give reason for incomplete.',
            form.errors.get('__all__'))
