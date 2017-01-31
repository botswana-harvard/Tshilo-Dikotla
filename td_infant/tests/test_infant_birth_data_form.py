from django import forms
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from edc_constants.constants import SCREENED
from edc_registration.models import RegisteredSubject
from edc_identifier.models import SubjectIdentifier
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, POS, YES, NO, NOT_APPLICABLE
from edc_meta_data.models import RequisitionMetaData
from edc_appointment.models import Appointment

from td_maternal.models import MaternalVisit

from td_maternal.tests import BaseTestCase
from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabourDelFactory,
                                         MaternalVisitFactory)
from td_infant.forms import InfantBirthDataForm
from .factories import InfantBirthFactory, InfantVisitFactory


class TestInfantBirthData(BaseTestCase):

    def setUp(self):
        super(TestInfantBirthData, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

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
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)
        self.antenatal_visit_1 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1010M'))
        self.antenatal_visit_2 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1020M'))
        self.maternal_visit_2000 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='2000M'))

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.options = {
            'report_datetime': timezone.now(),
            'infant_visit': self.infant_visit,
            'weight_kg': 3.61,
            'infant_length': 89.97,
            'head_circumference': 39.30,
            'apgar_score': NO,
            'apgar_score_min_1': '',
            'apgar_score_min_5': '',
            'apgar_score_min_10': '',
            'congenital_anomalities': NO}

    def test_infant_length(self):
            self.options['infant_birth'] = self.infant_visit.id
            self.options['infant_length'] = 95.62
            self.assertRaises(forms.ValidationError)

    def test_validate_infant_head_cir(self):
        self.options['infant_birth'] = self.infant_visit.id
        self.options['head_circumference'] = 41.23
        self.assertRaises(forms.ValidationError)

    def test_validate_apgar_1(self):
        self.options['apgar_score'] = YES
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored performed, then you should answer At 1 minute', errors)

    def test_validate_apgar_2(self):
        self.options['apgar_score'] = YES
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored performed, then you should answer At 1 minute', errors)

    def test_validate_apgar_3(self):
        self.options['apgar_score'] = YES
        self.options['apgar_score_min_1'] = 3
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored performed, then you should answer At 5 minute', errors)

    def test_validate_apgar_4(self):
        self.options['apgar_score'] = NO
        self.options['apgar_score_min_1'] = 3
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored was NOT performed, then you should NOT answer at 1 minute', errors)

    def test_validate_apgar_5(self):
        self.options['apgar_score'] = NO
        self.options['apgar_score_min_5'] = 3
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored was NOT performed, then you should NOT answer at 5 minute', errors)

    def test_validate_apgar_6(self):
        self.options['apgar_score'] = NO
        self.options['apgar_score_min_10'] = 3
        form = InfantBirthDataForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If Apgar scored was NOT performed, then you should NOT answer at 10 minute', errors)
