from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from edc_constants.constants import SCREENED
from td_registration.models import RegisteredSubject
from edc_identifier.models import SubjectIdentifier
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, POS, YES, NO, NOT_APPLICABLE
from edc_meta_data.models import RequisitionMetaData

from td_appointment.models import Appointment

from td_maternal.models import MaternalVisit

from td_maternal.tests import BaseTestCase
from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabourDelFactory,
                                         MaternalVisitFactory)
from td_infant.forms import InfantFuDxItemsForm
from .factories import InfantBirthFactory, InfantVisitFactory, InfantFuFactory, InfantFuDxFactory


class TestInfantFuDxItemsForm(BaseTestCase):

    def setUp(self):
        super(TestInfantFuDxItemsForm, self).setUp()
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
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.infant_fu_factory = InfantFuFactory(was_hospitalized=YES, infant_visit=self.infant_visit)
        self.infant_fu_dx_factory = InfantFuDxFactory(infant_visit=self.infant_visit)
        self.options = {'infant_vist': self.infant_visit,
                        'infant_fu_dx': self.infant_fu_dx_factory.id,
                        'fu_dx': 'Appendicitis',
                        'fu_dx_specify': None,
                        'health_facility': YES,
                        'was_hospitalized': YES,
                        }

    def test_validate_seen_at_health_facility(self):
        """Test validate if the participant was hospitalized and seen at a health facility"""
        self.options['was_hospitalized'] = YES
        self.options['health_facility'] = NO
        infant_fu_dx_items = InfantFuDxItemsForm(data=self.options)
        self.assertIn(
            'You indicated that participant was hospitalized, therefore the participant '
            'was seen at a health facility. Please correct.',
            infant_fu_dx_items.errors.get('__all__'))

    def test_validate_reported_hospitalization(self):
        """Test validate if Question6 on Infant Follow Up form is answered YES"""
        self.infant_fu_factory.was_hospitalized = NO
        self.infant_fu_factory.save()
        self.options['infant_fu_dx'] = self.infant_fu_dx_factory.id
        infant_fu_dx_items = InfantFuDxItemsForm(data=self.options)
        self.assertIn('Question6 in Infant Follow Up is not answered YES, you cannot fill this form.',
                      infant_fu_dx_items.errors.get('__all__'))

    def test_validate_other_serious_grade3or4_infection_specification(self):
        """Test if diagnosis specification for infections is provided"""
        self.options['fu_dx'] = 'Other serious (grade 3 or 4)infection(not listed above),specify'
        self.options['fu_dx_specify'] = None
        infant_fu_dx = InfantFuDxItemsForm(data=self.options)
        self.assertIn('You mentioned there is other serious (grade 3 or 4) infection, Please specify',
                      infant_fu_dx.errors.get('__all__'))

    def test_other_serious_grade3or4_non_infectious_specification(self):
        """Test if diagnosis specification for non-infectious is provided"""
        self.options['fu_dx'] = 'Other serious (grade 3 or 4) non-infectious(not listed above),specify'
        self.options['fu_dx_specify'] = None
        infant_fu_dx = InfantFuDxItemsForm(data=self.options)
        self.assertIn('You mentioned there is other serious (grade 3 or 4) non-infectious, Please specify',
                      infant_fu_dx.errors.get('__all__'))

    def test_other_abnormallaboratory_tests_specification(self):
        """Test if test and result of other abnormal laboratory is provided"""
        self.options['fu_dx'] = 'Other abnormallaboratory tests(other than tests listed above ''or tests done as part of this study), specify test and result'
        self.options['fu_dx_specify'] = None
        infant_fu_dx = InfantFuDxItemsForm(data=self.options)
        self.assertIn('You mentioned there is abnormallaboratory tests, Please specify',
                      infant_fu_dx.errors.get('__all__'))

    def test_validate_new_congenital_abnormality_not_previously_identified_specification(self):
        """Test if new congenital abnormality not previously identified is specified'"""
        self.options['fu_dx'] = 'New congenital abnormality not previously identified?,specify'
        self.options['fu_dx_specify'] = None
        infant_fu_dx = InfantFuDxItemsForm(data=self.options)
        self.assertIn('You mentioned there is new congenital abnormality not previously identified , Please specify',
                      infant_fu_dx.errors.get('__all__'))
