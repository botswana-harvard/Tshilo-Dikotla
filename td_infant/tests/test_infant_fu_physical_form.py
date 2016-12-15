from dateutil.relativedelta import relativedelta
from django.test import TestCase
from model_mommy import mommy

from edc_visit_tracking.constants import SCHEDULED
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NO

from td.models import Appointment

from td_infant.forms import InfantFuPhysicalForm

from .test_mixins import InfantMixin


class TestInfantFuPhysicalForm(InfantMixin, TestCase):

    def setUp(self):
        super(TestInfantFuPhysicalForm, self).setUp()
        self.make_infant_birth(maternal_status=POS)
        infant_appointment_2000 = Appointment.objects.get(subject_identifier=self.infant_identifier, visit_code='2000')
        mommy.make_recipe(
            'td_infant.infantvisit',
            appointment=infant_appointment_2000,
            report_datetime=infant_appointment_2000.appt_datetime,
            reason=SCHEDULED)

        infant_appointment_2010 = Appointment.objects.get(subject_identifier=self.infant_identifier, visit_code='2010')
        mommy.make_recipe(
            'td_infant.infantvisit',
            appointment=infant_appointment_2010,
            report_datetime=infant_appointment_2010.appt_datetime,
            reason=SCHEDULED)
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=NO)

        self.infant_fu = mommy.make_recipe(
            'td_infant.infantfu',
            infant_visit=self.get_infant_visit('2010'),
            was_hospitalized=YES)

        infant_appointment_2020 = Appointment.objects.get(subject_identifier=self.infant_identifier, visit_code='2020')
        mommy.make_recipe(
            'td_infant.infantvisit',
            appointment=infant_appointment_2020,
            report_datetime=infant_appointment_2020.appt_datetime,
            reason=SCHEDULED)

        self.options = {
            'infant_visit': self.get_infant_visit('2020').id,
            'report_datetime': get_utcnow(),
            'weight_kg': 3,
            'height': 45.01,
            'head_circumference': 18.01,
            'general_activity': "NORMAL",
            'physical_exam_result': "NORMAL",
            'heent_exam': YES,
            'resp_exam': YES,
            'cardiac_exam': YES,
            'abdominal_exam': YES,
            'skin_exam': YES,
            'neurologic_exam': YES,
        }

    def test_validate_infant_height(self):
        mommy.make_recipe(
            'td_infant.infantfuphysical',
            infant_visit=self.get_infant_visit('2010'),
            height=45.01)
        self.options.update(height=15.01)
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            u'You stated that the height for the participant as {}, yet in visit {} '
            'you indicated that participant height was {}. Please correct.'.format(
                self.options['height'], '2010', 45.01),
            infant_fu_physical.errors.get('__all__'))

    def test_validate_infant_head_circumference(self):
        mommy.make_recipe(
            'td_infant.infantfuphysical',
            infant_visit=self.get_infant_visit('2010'))
        self.options.update(head_circumference=15.01)
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            u'You stated that the head circumference for the participant as {}, '
            'yet in visit {} you indicated that participant height was {}. Please correct.'.format(
                self.options['head_circumference'], '2010', 18.01), infant_fu_physical.errors.get('__all__'))

    def test_validate_infant_report_datetime(self):
        self.options['report_datetime'] = (self.infant_birth.dob - relativedelta(years=1))
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            u'Report date {} cannot be before infant DOB of {}'.format(
                self.options['report_datetime'],
                self.infant_birth.dob), infant_fu_physical.errors.get('__all__'))

    def test_validate_general_activity(self):
        self.options.update(
            general_activity='ABNORMAL',
            abnormal_activity=None)
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn('If abnormal, please specify.', infant_fu_physical.errors.get('__all__'))

    def test_validate_no_general_activity(self):
        self.options.update(
            general_activity=None,
            abnormal_activity='Fingers')
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that there was NO abnormality in general activity, yet '
            'specified abnormality. Please correct', infant_fu_physical.errors.get('__all__'))

    def test_validate_heent_exam(self):
        self.options.update(heent_no_other='Eyes')
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If HEENT Exam is normal, Do not answer the following Question (Q10).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_heent_exam(self):
        self.options.update(heent_exam=NO, heent_no_other=None)
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that HEENT exam was not normal. Provide answer to Q10.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_resp_exam(self):
        self.options.update(resp_exam_other='Breathing')
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Respiratory Exam is normal, Do not answer the following Question (Q12).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_resp_exam(self):
        self.options.update(resp_exam=NO, resp_exam_other=None)
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Respiratory exam was not normal. Provide answer to Q12.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_cardiac_exam(self):
        self.options.update(cardiac_exam_other='Arythmia')
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Cardiac Exam is normal, Do not answer the following Question (Q14).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_cardiac_exam(self):
        self.options.update(cardiac_exam=NO, cardiac_exam_other=None)
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Cardiac exam was not normal. Provide answer to Q14.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_abdominal_exam(self):
        self.options.update(abdominal_exam_other='Diarrohea')
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Abdominal Exam is normal, Do not answer the following Question (Q16).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_abdominal_exam(self):
        self.options.update(
            abdominal_exam=NO,
            abdominal_exam_other=None)
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Abdominal exam was not normal. Provide answer to Q16.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_skin_exam(self):
        self.options.update(skin_exam_other='Eczema')
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Skin Exam is normal, Do not answer the following Question (Q18).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_skin_exam(self):
        self.options.update(skin_exam=NO, skin_exam_other=None)
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Skin exam was not normal. Provide answer to Q18.',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_neurologic_exam(self):
        self.options.update(neuro_exam_other='Down Syndrome')
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'If Neurological Exam is normal, Do not answer the following Question (Q22).',
            infant_fu_physical.errors.get('__all__'))

    def test_validate_no_neurologic_exam(self):
        self.options.update(neurologic_exam=NO, neuro_exam_other=None)
        infant_fu_physical = InfantFuPhysicalForm(data=self.options)
        self.assertIn(
            'You indicated that Neurological exam was not normal. Provide answer to Q22.',
            infant_fu_physical.errors.get('__all__'))
