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
from td_infant.forms import InfantNvpDispensingForm
from .factories import InfantBirthFactory, InfantVisitFactory


class TestInfantNvpDispensingForm(BaseTestCase):

    def setUp(self):
        super(InfantNvpDispensingForm, self).setUp()
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
            'infant_visit': self.infant_visit.id,
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'nvp_admin_date': timezone.now().date(),
            'medication_instructions': YES,
            'dose_admin_infant': '10',
            'correct_dose': YES
        }

    def test_validate_nvp_prohylaxis_yes_azt_prophylaxis_none(self):
        self.options.update(nvp_prophylaxis=YES, azt_prophylaxis=None)
        form = InfantNvpDispensingForm(data=self.options)
        self.assertIn(
            u'Was the infant given AZT infant prophylaxis? Please answer YES or NO.',
            form.errors.get('__all__'))

    def test_validate_nvp_prohylaxis_yes_reason_not_given_not_none(self):
        self.options.update(nvp_prophylaxis=YES, reason_not_given='Medication spilled.')
        form = InfantNvpDispensingForm(data=self.options)
        self.assertIn(
            u'Infant received NVP prophylaxis, do not give reason.',
            form.errors.get('__all__'))

    def test_validate_nvp_prohylaxis_yes_nvp_admin_date_none(self):
        self.options.update(nvp_prophylaxis=YES, nvp_admin_date=None)
        form = InfantNvpDispensingForm(data=self.options)
        self.assertIn(
            u'Please give the NVP infant prophylaxis date.',
            form.errors.get('__all__'))

    def test_validate_nvp_prohylaxis_yes_medication_instructions_none(self):
        self.options.update(nvp_prophylaxis=YES, medication_instructions=None)
        form = InfantNvpDispensingForm(data=self.options)
        self.assertIn(
            u'If the Infant received NVP prophylaxis, was the mother '
            'given instructions on how to administer the medication?',
            form.errors.get('__all__'))

    def test_validate_nvp_prohylaxis_yes_dose_admin_infant_none(self):
        self.options.update(nvp_prophylaxis=YES, dose_admin_infant=None)
        form = InfantNvpDispensingForm(data=self.options)
        self.assertIn(
            u'Please give the NVP prophylaxis dosage information.',
            form.errors.get('__all__'))

    def test_validate_nvp_prohylaxis_yes_correct_dose_none(self):
        self.options.update(nvp_prophylaxis=YES, correct_dose=None)
        form = InfantNvpDispensingForm(data=self.options)
        self.assertIn(
            u'Was the correct NVP prophylaxis dose given?',
            form.errors.get('__all__'))

    def test_validate_nvp_prohylaxis_no_reason_not_given_none(self):
        self.options.update(nvp_prophylaxis=NO, reason_not_given=None)
        form = InfantNvpDispensingForm(data=self.options)
        self.assertIn(
            u'Infant did NOT receive NVP infant prophylaxis, please give a reason.',
            form.errors.get('__all__'))

    def test_validate_azt_prophylaxis_yes_azt_dose_given_none(self):
        self.options.update(azt_prophylaxis=YES, azt_dose_given=None)
        form = InfantNvpDispensingForm(data=self.options)
        self.assertIn(
            u'Infant received AZT prophylaxis, please give the dose administered.',
            form.errors.get('__all__'))

    def test_validate_azt_prophylaxis_no_azt_dose_given_not_none(self):
        self.options.update(azt_prophylaxis=NO, azt_dose_given='1 teaspoon per day.')
        form = InfantNvpDispensingForm(data=self.options)
        self.assertIn(
            u'Infant did NOT receive AZT prophylaxis, please do not give the dose.',
            form.errors.get('__all__'))
