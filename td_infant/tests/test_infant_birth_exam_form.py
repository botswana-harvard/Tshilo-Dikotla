from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, POS

from td_infant.forms import InfantBirthExamForm
from .test_mixins import InfantMixin


class TestInfantBirthExam(InfantMixin, TestCase):

    def setUp(self):
        super(TestInfantBirthExam, self).setUp()
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visit('2000', 'scheduled')
        infant_visit = self.get_infant_visit('2000')
        self.options = {
            'report_datetime': get_utcnow(),
            'infant_visit': infant_visit.id,
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
        self.options.update(
            general_activity='ABNORMAL',
            abnormal_activity=None)
        self.infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'If abnormal, please specify.', errors)

    def test_validate_general_activity2(self):
        self.options.update(
            general_activity='NORMAL',
            abnormal_activity='looks sideways')
        self.infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'You indicated that there was NO abnormality in general activity', errors)

    def test_validate_heent_exam1(self):
        self.options.update(
            heent_exam=YES,
            heent_no_other='HEENT problems')
        self.infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'If HEENT Exam is normal, Do not answer the following Question (Q7).', errors)

    def test_validate_heent_exam2(self):
        self.options.update(heent_exam=NO)
        self.infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q7.', errors)

    def test_validate_resp_exam1(self):
        self.options.update(
            resp_exam=YES,
            resp_exam_other='Asthma')
        self.infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'If Respiratory Exam is normal, Do not answer the following Question (Q9).', errors)

    def test_validate_resp_exam2(self):
        self.options.update(resp_exam=NO)
        self.infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q9.', errors)

    def test_validate_cardiac_exam1(self):
        self.options.update(
            cardiac_exam=YES,
            cardiac_exam_other='Palpitations')
        self.infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'If Cardiac Exam is normal, Do not answer the following Question (Q11).', errors)

    def test_validate_cardiac_exam2(self):
        self.options.update(cardiac_exam=NO)
        self.infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q11.', errors)

    def test_validate_report_datetime_invalid(self):
        self.options.update(
            report_datetime=get_utcnow() - relativedelta(years=34))
        self.infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(self.infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'Report_Datetime CANNOT be before consent datetime', errors)

    def test_abdominal_exam_1(self):
        self.options.update(abdominal_exam=NO)
        infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q13.', errors)

    def test_abdominal_exam_2(self):
        self.options.update(
            abdominal_exam=YES,
            abdominal_exam_other='TOO BIG')
        infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'If Abdominal Exam is normal', errors)

    def test_skin_exam_1(self):
        self.options.update(skin_exam=NO)
        infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q15.', errors)

    def test_skin_exam_2(self):
        self.options.update(
            skin_exam=YES,
            skin_exam_other='lesions')
        infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'If Skin Exam is normal', errors)

    def test_neuro_exam_1(self):
        self.options.update(
            neurologic_exam=YES,
            neuro_exam_other='bipolar')
        infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'If Neurological Exam is normal', errors)

    def test_neuro_exam_2(self):
        self.options.update(neurologic_exam=NO)
        infant_birth_exam = InfantBirthExamForm(data=self.options)
        errors = ''.join(infant_birth_exam.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q19.', errors)
