from dateutil.relativedelta import relativedelta
from datetime import date
from django.utils import timezone

from edc_constants.constants import SCREENED
from td_registration.models import RegisteredSubject
from edc_constants.constants import POS, YES, NO, NOT_APPLICABLE, UNKNOWN
from td_appointment.models import Appointment

from tshilo_dikotla.constants import MODIFIED, NO_MODIFICATIONS, DISCONTINUED, NEVER_STARTED

from td_maternal.tests import BaseTestCase
from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabourDelFactory,
                                         MaternalVisitFactory)
from td_infant.forms import InfantArvProphForm, InfantArvProphModForm
from .factories import InfantBirthFactory, InfantVisitFactory, InfantArvProphFactory, InfantBirthArvFactory


class TestInfantArvProph(BaseTestCase):

    def setUp(self):
        super(TestInfantArvProph, self).setUp()
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
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)

        self.antenatal_visits_membership = AntenatalVisitMembershipFactory(
            registered_subject=options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=options.get('registered_subject'), visit_code='1010M')

        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(RegisteredSubject.objects.all()[0].__dict__)
        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.infant_birth_arv = InfantBirthArvFactory(infant_visit=self.infant_visit, azt_discharge_supply=YES)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': self.infant_visit.id,
            'prophylatic_nvp': YES,
            'arv_status': MODIFIED,
        }

    def test_validate_taking_arv_proph_no(self):
        """Test if the infant was not taking prophylactic arv and arv status is not Not Applicable"""
        self.data['prophylatic_nvp'] = NO
        self.data['arv_status'] = MODIFIED
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(u'Infant was not taking prophylactic arv, prophylaxis should be Never Started or Discontinued.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_taking_arv_proph_discontinued(self):
        """Test if the was not taking  prophylactic arv and infant was not given arv's at birth"""
        self.infant_birth_arv.azt_discharge_supply = UNKNOWN
        self.infant_birth_arv.save()
        self.data['prophylatic_nvp'] = NO
        self.data['arv_status'] = DISCONTINUED
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(
            u'The azt discharge supply in Infant birth arv was answered as NO or Unknown, '
            'therefore Infant ARV proph in this visit cannot be permanently discontinued.',
            infant_arv_proph.errors.get('__all__'))

    def test_validate_taking_arv_proph_yes(self):
        """Test if the infant was not taking prophylactic arv and arv status is Never Started"""
        self.data['prophylatic_nvp'] = YES
        self.data['arv_status'] = NEVER_STARTED
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(u'Infant has been on prophylactic arv, cannot choose Never Started or Permanently discontinued.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_dose_status(self):
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': None,
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You entered an ARV Code, please give the dose status.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_date(self):
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': 'New',
                       'modification_date': None,
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You entered an ARV Code, please give the modification date.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_code(self):
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': None}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You entered an ARV Code, please give the modification reason.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_not_needed(self):
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=NO_MODIFICATIONS)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You did NOT indicate that medication was modified, so do not ENTER arv inline.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_azt_initiated(self):
        """Check that the azt dose is not initiated more than once"""
        self.infant_birth_arv.azt_discharge_supply = YES
        self.infant_birth_arv.save()
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Zidovudine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(
            u'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
            'AZT cannot be initiated again.',
            infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_azt_different(self):
        """Check that the dose being modified is the same one infant was discharged with."""
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevarapine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(
            u'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
            'Arv Code should be AZT',
            infant_arv_proph.errors.get('__all__'))
