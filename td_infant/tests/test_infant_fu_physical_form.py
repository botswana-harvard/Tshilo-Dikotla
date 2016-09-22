from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from edc_constants.constants import SCREENED
from td_registration.models import RegisteredSubject
from edc_identifier.models import SubjectIdentifier
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, POS, YES, NO, NOT_APPLICABLE, UNKNOWN
from edc_meta_data.models import RequisitionMetaData

from td_appointment.models import Appointment

from tshilo_dikotla.constants import MODIFIED, NO_MODIFICATIONS, DISCONTINUED, NEVER_STARTED
from td_maternal.models import MaternalVisit

from td_maternal.tests import BaseTestCase
from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabourDelFactory,
                                         MaternalVisitFactory)
from td_infant.forms import InfantFuPhysicalForm
from .factories import InfantBirthFactory, InfantVisitFactory, InfantArvProphFactory, InfantBirthArvFactory, InfantFuPhysicalFactory


class TestInfantFuPhysicalForm(BaseTestCase):

    def setUp(self):
        super(TestInfantFuPhysicalForm, self).setUp()
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
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')

        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.infant_fu = InfantFuPhysicalFactory(infant_visit=self.infant_visit)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2020')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.options = {
            'infant_visit': self.infant_visit.id,
            'report_datetime': timezone.now(),
            'weight_kg': 3,
            'height': 45.01,
            'head_circumference': 18.01,
            'general_activity': "NORMAL",
            'physical_exam_result': "NORMAL",
            'heent_exam': YES,
            'was_hospitalized': YES,
            'resp_exam': YES,
            'cardiac_exam': YES,
            'abdominal_exam': YES,
            'skin_exam': YES,
            'neurologic_exam': YES,
        }

    def test_validate_infant_height(self):
        self.infant_fu.height = 45.01
        self.infant_fu.save()
        self.options['height'] = 15.01
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            u'You stated that the height for the participant as {}, yet in visit {} '
            'you indicated that participant height was {}. Please correct.'.format(
            self.options['height'], '2010', 45.01),
            infant_fu_physical.errors.get('__all__'))

    def test_validate_infant_head_circumference(self):
        self.infant_fu.head_circumference = 18.01
        self.infant_fu.save()
        self.options['head_circumference'] = 15.01
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            u'You stated that the head circumference for the participant as {}, '
            'yet in visit {} you indicated that participant height was {}. Please correct.'.format(
            self.options['head_circumference'], '2010', 18.01), infant_fu_physical.errors.get('__all__'))

    def test_validate_infant_report_datetime(self):
        self.options['report_datetime'] = (timezone.datetime.now() - relativedelta(years=1)).date()
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            u'Report date {} cannot be before infant DOB of {}'.format(
                    self.options['report_datetime'],
                    self.infant_visit.appointment.registered_subject.dob), infant_fu_physical.errors.get('__all__'))

    def test_validate_general_activity(self):
        self.options['general_activity'] = 'ABNORMAL'
        self.options['abnormal_activity'] = None
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn('If abnormal, please specify.', infant_fu_physical.errors.get('__all__'))

    def test_validate_no_general_activity(self):
        self.options['general_activity'] = None
        self.options['abnormal_activity'] = 'Fingers'
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that there was NO abnormality in general activity, yet '
            'specified abnormality. Please correct', infant_fu_physical.errors.get('__all__'))

    def test_validate_heent_exam(self):
        self.options['heent_no_other'] = 'Eyes'
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If HEENT Exam is normal, Do not answer the following Question (Q10).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_heent_exam(self):
        self.options['heent_exam'] = NO
        self.options['heent_no_other'] = None
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that HEENT exam was not normal. Provide answer to Q10.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_resp_exam(self):
        self.options['resp_exam_other'] = 'Breathing'
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Respiratory Exam is normal, Do not answer the following Question (Q12).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_resp_exam(self):
        self.options['resp_exam'] = NO
        self.options['resp_exam_other'] = None
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Respiratory exam was not normal. Provide answer to Q12.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_cardiac_exam(self):
        self.options['cardiac_exam_other'] = 'Arythmia'
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Cardiac Exam is normal, Do not answer the following Question (Q14).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_cardiac_exam(self):
        self.options['cardiac_exam'] = NO
        self.options['cardiac_exam_other'] = None
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Cardiac exam was not normal. Provide answer to Q14.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_abdominal_exam(self):
        self.options['abdominal_exam_other'] = 'Diarrohea'
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Abdominal Exam is normal, Do not answer the following Question (Q16).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_abdominal_exam(self):
        self.options['abdominal_exam'] = NO
        self.options['abdominal_exam_other'] = None
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Abdominal exam was not normal. Provide answer to Q16.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_skin_exam(self):
        self.options['skin_exam_other'] = 'Eczema'
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Skin Exam is normal, Do not answer the following Question (Q18).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_skin_exam(self):
        self.options['skin_exam'] = NO
        self.options['skin_exam_other'] = None
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Skin exam was not normal. Provide answer to Q18.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_neurologic_exam(self):
        self.options['neuro_exam_other'] = 'Down Syndrome'
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Neurological Exam is normal, Do not answer the following Question (Q22).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_neurologic_exam(self):
        self.options['neurologic_exam'] = NO
        self.options['neuro_exam_other'] = None
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Neurological exam was not normal. Provide answer to Q22.',
            infant_fu_physical.errors.get('__all__'))
