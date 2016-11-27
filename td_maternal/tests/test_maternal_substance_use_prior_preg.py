from dateutil.relativedelta import relativedelta
from django.utils import timezone
from model_mommy import mommy

from edc_constants.constants import UNKNOWN, YES, NO, NEG, NOT_APPLICABLE

from td_maternal.models import Appointment
from td_maternal.forms import MaternalSubstanceUsePriorPregForm

from .base_test_case import BaseTestCase


class TestMaternalSubstanceUsePriorPreg(BaseTestCase):

    def setUp(self):
        super(TestMaternalSubstanceUsePriorPreg, self).setUp()
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
            'smoked_prior_to_preg': YES,
            'smoking_prior_preg_freq': 'daily',
            'alcohol_prior_pregnancy': YES,
            'alcohol_prior_preg_freq': 'daily',
            'marijuana_prior_preg': YES,
            'marijuana_prior_preg_freq': 'daily',
            'other_illicit_substances_prior_preg': None}

    def test_smoked_prior_to_pregnancy_yes(self):
        self.options['smoking_prior_preg_freq'] = None
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has smoked tobacco prior to this pregnancy, please give a frequency.', errors)

    def test_smoked_prior_to_pregnancy_no(self):
        self.options['smoked_prior_to_preg'] = NO
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never smoked tobacco prior to this pregnancy, please do not give a frequency.', errors)

    def test_alcohol_prior_pregnancy_yes(self):
        self.options['alcohol_prior_preg_freq'] = None
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has drank alcohol prior this pregnancy, please give a frequency.', errors)

    def test_alcohol_prior_pregnancy_no(self):
        self.options['alcohol_prior_pregnancy'] = NO
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never drank alcohol prior this pregnancy, please do not give a frequency.', errors)

    def test_marijuana_prior_preg_yes(self):
        self.options['marijuana_prior_preg_freq'] = None
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Participant has smoked marijuana prior to this pregnancy, please give a frequency.', errors)

    def test_marijuana_prior_preg_no(self):
        self.options['marijuana_prior_preg'] = NO
        form = MaternalSubstanceUsePriorPregForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has never smoked marijuana prior to this pregnancy, please do not give a frequency.', errors)
