from dateutil.relativedelta import relativedelta
from django.utils import timezone

from td.models import Appointment
from td.models import RegisteredSubject
from edc_constants.constants import (YES, NOT_APPLICABLE, POS, NO)
from edc_code_lists.models import WcsDxAdult

from td_list.models import MaternalDiagnoses
from td_maternal.forms import MaternalDiagnosesForm

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, MaternalVisitFactory, AntenatalVisitMembershipFactory,
                        MaternalLabourDelFactory)


class TestMaternalDiagnosesForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalDiagnosesForm, self).setUp()
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
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        MaternalLabourDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        self.maternal_visit_2000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.diagnoses = MaternalDiagnoses.objects.create(
            hostname_created="django", name="Gestational Hypertension",
            short_name="Gestational Hypertension", created=timezone.datetime.now(),
            user_modified="", modified=timezone.datetime.now(),
            hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None,
            revision=":develop:")

        self.diagnoses_na = MaternalDiagnoses.objects.create(
            hostname_created="django", name="Not Applicable",
            short_name="N/A", created=timezone.datetime.now(),
            user_modified="", modified=timezone.datetime.now(),
            hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None,
            revision=":develop:")

        self.who_dx = WcsDxAdult.objects.create(
            hostname_created="cabel", code="CS4003", short_name="Recurrent severe bacterial pneumo",
            created=timezone.datetime.now(), user_modified="", modified=timezone.datetime.now(), hostname_modified="cabel",
            long_name="Recurrent severe bacterial pneumonia", user_created="abelc",
            list_ref="WHO CLINICAL STAGING OF HIV INFECTION 2006", revision=None)

        self.who_dx_na = WcsDxAdult.objects.create(
            hostname_created="cabel", code="CS4002", short_name="N/A",
            created=timezone.datetime.now(), user_modified="", modified=timezone.datetime.now(), hostname_modified="cabel",
            long_name="Not Applicable", user_created="abelc", 
            list_ref="WHO CLINICAL STAGING OF HIV INFECTION 2006", revision=None)

        self.options = {
            'maternal_visit': self.maternal_visit_2000,
            'new_diagnoses': YES,
            'diagnoses': [self.diagnoses.id],
            'has_who_dx': YES,
            'who': [self.who_dx.id]}

    def test_has_diagnoses_no_dx(self):
        self.options['diagnoses'] = None
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has new diagnoses, please give a diagnosis.', errors)

    def test_has_diagnoses_not_applicable_selected(self):
        self.options['diagnoses'] = [self.diagnoses.id, self.diagnoses_na.id]
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('New Diagnoses is Yes, diagnoses list cannot have Not Applicable. Please correct.', errors)

    def test_has_no_dx_but_listed(self):
        self.options['new_diagnoses'] = NO
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant does not have any new diagnoses, new diagnosis should be Not Applicable.', errors)

    def test_has_no_dx_but_listed_with_not_applicable(self):
        self.options['new_diagnoses'] = NO
        self.options['diagnoses'] = [self.diagnoses.id, self.diagnoses_na.id]
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant does not have any new diagnoses, new diagnosis should be Not Applicable.', errors)

    def test_has_who_diagnosis(self):
        self.options['who'] = None
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('WHO diagnosis is Yes, please give who diagnosis.', errors)

    def test_has_who_diagnosis_not_applicable_selected(self):
        self.options['who'] = [self.who_dx.id, self.who_dx_na.id]
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('WHO Stage III/IV cannot have Not Applicable in the list. Please correct.', errors)

    def test_has_now_who_dx_but_listed(self):
        self.options['has_who_dx'] = NO
        form = MaternalDiagnosesForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'WHO diagnoses is {}, WHO Stage III/IV should be Not Applicable.'.format(self.options['has_who_dx']), 
            errors)
