from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.utils import timezone

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NO, NOT_APPLICABLE
from edc_registration.models import RegisteredSubject

from td.models import Appointment

from td_maternal.tests import BaseTestCase
from td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                         MaternalConsentFactory, AntenatalEnrollmentFactory,
                                         AntenatalVisitMembershipFactory, MaternalLabDelFactory,
                                         MaternalVisitFactory)
from td_infant.forms import InfantBirthExamForm
from .factories import InfantBirthFactory, InfantVisitFactory


class TestInfantBirthExam(BaseTestCase):

    def setUp(self):
        super(TestInfantBirthExam, self).setUp()
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

        self.maternal_labour_del = MaternalLabDelFactory(registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type='infant')

        self.assertTrue(RegisteredSubject.objects.all().count(), 2)

        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)

        self.appointment = Appointment.objects.get(
            subject_identifier=infant_registered_subject.subject_identifier, visit_code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)

        self.options = {
            'report_datetime': get_utcnow(),
            'infant_birth': self.infant_birth.id,
            'infant_visit': self.infant_visit.id,
            'infant_exam_date': get_utcnow().date(),
            'general_activity': 'NORMAL',
            'abnormal_activity': '',
            'physical_exam_result': 'NORMAL',
            'heent_exam': YES,
            'heent_no_other': '',
            'resp_exam': YES,
            'resp_exam_other': '',
            'cardiac_exam': YES,
            'cardiac_exam_other': '',
            'abdominal_exam': YES,
            'abdominal_exam_other': '',
            'skin_exam': YES,
            'skin_exam_other': '',
            'neurologic_exam': YES,
            'neuro_exam_other': '',
            'other_exam_info': 'NA'}

    def test_validate_general_activity1(self):
        self.options['general_activity'] = 'ABNORMAL'
        self.options['abnormal_activity'] = ''
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If abnormal, please specify.', errors)

    def test_validate_general_activity2(self):
        self.options['general_activity'] = 'NORMAL'
        self.options['abnormal_activity'] = 'looks sideways'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'You indicated that there was NO abnormality in general activity', errors)

    def test_validate_heent_exam1(self):
        self.options['heent_exam'] = YES
        self.options['heent_no_other'] = 'HEENT problems'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If HEENT Exam is normal, Do not answer the following Question (Q7).', errors)

    def test_validate_heent_exam2(self):
        self.options['heent_exam'] = NO
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q7.', errors)

    def test_validate_resp_exam1(self):
        self.options['resp_exam'] = YES
        self.options['resp_exam_other'] = 'Asthma'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Respiratory Exam is normal, Do not answer the following Question (Q9).', errors)

    def test_validate_resp_exam2(self):
        self.options['resp_exam'] = NO
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q9.', errors)

    def test_validate_cardiac_exam1(self):
        self.options['cardiac_exam'] = YES
        self.options['cardiac_exam_other'] = 'Palpitations'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Cardiac Exam is normal, Do not answer the following Question (Q11).', errors)

    def test_validate_cardiac_exam2(self):
        self.options['cardiac_exam'] = NO
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q11.', errors)

    def test_validate_report_datetime_invalid(self):
        self.options['cardiac_exam'] = NO
        self.options['report_datetime'] = datetime(2015, 11, 18, 8, 29, 44)
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Report_Datetime CANNOT be before consent datetime', errors)

    def test_abdominal_exam_1(self):
        self.options['abdominal_exam'] = NO
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q13.', errors)

    def test_abdominal_exam_2(self):
        self.options['abdominal_exam'] = YES
        self.options['abdominal_exam_other'] = 'TOO BIG'
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Abdominal Exam is normal', errors)

    def test_skin_exam_1(self):
        self.options['skin_exam'] = NO
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q15.', errors)

    def test_skin_exam_2(self):
        self.options['skin_exam'] = YES
        self.options['skin_exam_other'] = 'lesions'
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Skin Exam is normal', errors)

    def test_neuro_exam_1(self):
        self.options['neurologic_exam'] = YES
        self.options['neuro_exam_other'] = 'bipolar'
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Neurological Exam is normal', errors)

    def test_neuro_exam_2(self):
        self.options['neurologic_exam'] = NO
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q19.', errors)
