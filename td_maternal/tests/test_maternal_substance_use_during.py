from dateutil.relativedelta import relativedelta
from django.utils import timezone
from model_mommy import mommy

from edc_constants.constants import UNKNOWN, YES, NO, NEG, NOT_APPLICABLE

from td.models import Appointment
from td_maternal.forms import MaternalSubstanceUseDuringPregForm

from .base_test_case import BaseTestCase


class TestMaternalSubstanceUseDuringPreg(BaseTestCase):

    def setUp(self):
        super(TestMaternalSubstanceUseDuringPreg, self).setUp()
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

        maternal_options = {
            'registered_subject': self.registered_subject,
            'current_hiv_status': UNKNOWN,
            'evidence_hiv_status': None,
            'week32_test': YES,
            'week32_test_date': (timezone.datetime.now() - relativedelta(weeks=4)).date(),
            'week32_result': NEG,
            'evidence_32wk_hiv_status': YES,
            'will_get_arvs': NOT_APPLICABLE,
            'rapid_test_done': YES,
            'rapid_test_result': NEG,
            'last_period_date': (timezone.datetime.now() - relativedelta(weeks=34)).date()}
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **maternal_options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit_1000, number_of_gestations=1)
        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership', registered_subject=maternal_options.get('registered_subject'))
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        self.antenatal_visit_2 = mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.options = {
            'maternal_visit': self.antenatal_visit_2.id,
            'smoked_during_pregnancy': YES,
            'smoking_during_preg_freq': 'daily',
            'alcohol_during_pregnancy': YES,
            'alcohol_during_preg_freq': 'daily',
            'marijuana_during_preg': YES,
            'marijuana_during_preg_freq': 'daily',
            'other_illicit_substances_during_preg': None}

    def test_smoked_during_pregnancy_yes(self):
        self.options['smoking_during_preg_freq'] = None
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has smoked tobacco during this pregnancy, please give a frequency.', errors)

    def test_smoked_during_pregnancy_no(self):
        self.options['smoked_during_pregnancy'] = NO
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never smoked tobacco during this pregnancy, please do not give a frequency.', errors)

    def test_alcohol_during_pregnancy_yes(self):
        self.options['alcohol_during_preg_freq'] = None
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has drank alcohol during this pregnancy, please give a frequency.', errors)

    def test_alcohol_during_pregnancy_no(self):
        self.options['alcohol_during_pregnancy'] = NO
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never drank alcohol during this pregnancy, please do not give a frequency.', errors)

    def test_marijuana_during_preg_yes(self):
        self.options['marijuana_during_preg_freq'] = None
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has smoked marijuana during this pregnancy, please give a frequency.', errors)

    def test_marijuana_during_preg_no(self):
        self.options['marijuana_during_preg'] = NO
        form = MaternalSubstanceUseDuringPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never smoked marijuana during this pregnancy, please do not give a frequency.', errors)
