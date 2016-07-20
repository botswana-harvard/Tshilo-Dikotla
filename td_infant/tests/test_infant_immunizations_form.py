from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from edc_constants.constants import SCREENED
from edc_registration.models import RegisteredSubject
from edc_identifier.models import SubjectIdentifier
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, POS, YES, NO, NOT_APPLICABLE, UNKNOWN
from edc_appointment.models import Appointment

from tshilo_dikotla.constants import MODIFIED, NO_MODIFICATIONS, DISCONTINUED, NEVER_STARTED
from td_maternal.models import MaternalVisit

from td_maternal.tests import BaseTestCase
from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabourDelFactory,
                                         MaternalVisitFactory)
from td_infant.forms import InfantFuImmunizationsForm, VaccinesReceivedForm
from .factories import InfantBirthFactory, InfantVisitFactory, InfantArvProphFactory, InfantBirthArvFactory


class TestInfantImmunizationForm(BaseTestCase):

    def setUp(self):
        super(TestInfantImmunizationForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

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
        self.maternal_visit_1100 = MaternalVisitFactory(
            appointment=Appointment.objects.get(registered_subject=options.get('registered_subject'),
                                                visit_definition__code='1100M'))

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
        self.infant_birth_arv = InfantBirthArvFactory(infant_visit=self.infant_visit, azt_discharge_supply=YES)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2100')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': self.infant_visit.id,
            'vaccines_received': YES,
            'vaccines_missed': NO
        }

    def test_vaccines_received_no_table_filling(self):
        """Test an infant who received vaccines but received vaccines table not filled"""
        form = InfantFuImmunizationsForm(data=self.data)
        self.assertIn("You mentioned that vaccines where received. Please"
                      " indicate which ones on the Received Vaccines table.",
                      form.errors.get('__all__'))

    def test_vaccines_missed_no_table_filling(self):
        """Test an infant who missed vaccines and missed vaccine table not filled"""
        self.data['vaccines_received'] = NO
        self.data['vaccines_missed'] = YES
        form = InfantFuImmunizationsForm(data=self.data)
        self.assertIn("You mentioned that the child missed some vaccines."
                      " Please indicate which ones in the Missed Vaccines "
                      "table.", form.errors.get('__all__'))

    def test_received_vaccine_fields(self):
        """Test that when a receive vaccine name is filled that a date is provided"""
        self.data['received_vaccine_name'] = 'BCG'
        self.data['date_given'] = ''
        self.data['infant_age'] = '2'
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("You provided a vaccine name {}. What date was it given to the "
                      "infant?".format(self.data['received_vaccine_name']), form.errors.get('__all__'))

    def test_missed_vaccine_fields(self):
        """Test that when a missed vaccine name is given that the reason should be provided"""
        self.data['missed_vaccine_name'] = 'BCG'
        self.data['reason_missed'] = ''
        form = VaccinesMissedForm(data=self.data)
        self.assertIn("You said {} vaccine was missed. Give a reason for missing this"
                      " vaccine".format(self.data['missed_vaccine_name']), form.errors.get('__all__'))

    def test_vaccination_at_birth(self):
        """Test that the correct vaccine is given at birth or few days after birth"""
        self.data['received_vaccine_name'] = 'BCG'
        self.data['infant_age'] = '2'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("BCG vaccination is ONLY given at birth or few days after birth",
                      form.errors.get('__all__'))

    def test_hepatitis_vaccine(self):
        """Test that the hepatitis vaccine is not given at inappropriate infant age"""
        self.data['received_vaccine_name'] = 'Hepatitis_B'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Hepatitis B can only be administered at birth or 2 or 3 or 4 "
                      "months of infant life", form.errors.get('__all__'))

    def test_dpt_vaccine(self):
        """Test that DPT vaccine is not given at inappropriate infant age"""
        self.data['received_vaccine_name'] = 'DPT'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("DPT. Diphtheria, Pertussis and Tetanus can only be admistered at"
                      " 2 or 3 or 4 months ONLY.", form.errors.get('__all__'))

    def test_haemophilus_vaccine(self):
        """Test that haemophilus influenza vaccine is not administered at inappropiate infant age"""
        self.data['received_vaccine_name'] = 'Haemophilus_influenza'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Haemophilus Influenza B vaccine can only be given at 2 or 3 or"
                      " 4 months of infant life.", form.errors.get('__all__'))

    def test_pcv_vaccine(self):
        """Test that PCV is administered at correct age"""
        self.data['received_vaccine_name'] = 'PCV_Vaccine'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("The PCV [Pneumonia Conjugated Vaccine], can ONLY be administered at"
                      " 2 or 3 or 4 months of infant life.", form.errors.get('__all__'))

    def test_polio_vaccine(self):
        """Test that polio vaccine is administered at correct age"""
        self.data['received_vaccine_name'] = 'Polio'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Polio vaccine can only be administered at 2 or 3 or 4 or 18 "
                      "months of infant life", form.errors.get('__all__'))

    def test_rotavirus_vaccine(self):
        """Test rotavirus administered to infant at age 4months"""
        self.data['received_vaccine_name'] = 'Rotavirus'
        self.data['infant_age'] = '4'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Rotavirus is only administered at 2 or 3 months of"
                      " infant life", form.errors.get('__all__'))

    def test_validate_measles_vaccine(self):
        """Test measles vaccine administered to an infant who is only a month old"""
        self.data['received_vaccine_name'] = 'Measles'
        self.data['infant_age'] = '2'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Measles vaccine is only administered at 9 or 18"
                      " months of infant life.", form.errors.get('__all__'))

    def test_pentavalent_vaccine(self):
        """Test for Pentavalent vaccine administered at 6-11 months of infant life"""
        self.data['received_vaccine_name'] = 'Pentavalent'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("The Pentavalent vaccine can only be administered at 2 or 3 or"
                      " 4 months of infant life.", form.errors.get('__all__'))

    def test_validate_vitamin_a_vaccine(self):
        """Test for Vitamin A vaccine administered earlier than 6 months"""
        self.data['received_vaccine_name'] = 'Vitamin_A'
        self.data['infant_age'] = '2'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Vitamin A is given to children between 6-11 months of"
                      " life", form.errors.get('__all__'))
