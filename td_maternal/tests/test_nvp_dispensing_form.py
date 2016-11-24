from dateutil.relativedelta import relativedelta
from datetime import date
from django.utils import timezone

from edc_constants.constants import (POS, YES, NO, NOT_APPLICABLE)
from td_appointment.models import Appointment

from td_maternal.tests import BaseTestCase

from ..forms import NvpDispensingForm

from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, MaternalVisitFactory, MaternalLabourDelFactory, AntenatalVisitMembershipFactory)


class TestNvpDispensingForm(BaseTestCase):

    def setUp(self):
        super(TestNvpDispensingForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

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

        self.maternal_delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        self.maternal_visit_2000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.options = {
            'maternal_visit': self.maternal_visit_2000,
            'maternal_delivery': self.maternal_delivery,
            'nvp_admin_date': date.today(),
            'medication_instructions': YES,
            'dose_admin_infant': '1 spoon per day',
            'correct_dose': YES,
            'corrected_dose': None,
            'dose_adjustment': YES,
            'week_2_dose': None
        }

    def test_validate_correct_dose_no(self):
        self.options['correct_dose'] = NO
        form = NvpDispensingForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If the correct dose was not given, please give the corrected dose.', errors)

    def test_validate_correct_dose_yes(self):
        self.options['corrected_dose'] = 'dose'
        form = NvpDispensingForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If the correct dose was given, please do not give the corrected dose.', errors)

    def test_week_2_dose_yes(self):
        form = NvpDispensingForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If infant came for a week 2 dose adjustment, please give the week 2 dose.', errors)

    def test_week_2_dose_no(self):
        self.options['dose_adjustment'] = NO
        self.options['week_2_dose'] = '2 spoons per day'
        form = NvpDispensingForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If infant did not come for a week 2 dose adjustment, '
            'please do not give the week 2 dose.', errors)