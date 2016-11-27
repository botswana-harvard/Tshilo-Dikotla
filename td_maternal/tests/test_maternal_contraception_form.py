from dateutil.relativedelta import relativedelta
from datetime import date
from django.utils import timezone
from model_mommy import mommy

from td.models import Appointment
from td.models import RegisteredSubject
from edc_constants.constants import (YES, NOT_APPLICABLE, POS, NO)

from td_list.models import Contraceptives, MaternalRelatives
from td_maternal.forms import MaternalContraceptionForm

from .base_test_case import BaseTestCase


class TestMaternalContraceptionForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalContraceptionForm, self).setUp()
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent', maternal_eligibility=self.maternal_eligibility)
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
        self.antenatal_enrollment = mommy.make_recipe('td_maternal.antenatalenrollment', **options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=self.maternal_visit, number_of_gestations=1,)

        self.antenatal_visits_membership = mommy.make_recipe(
            'td_maternal.antenatalvisitmembership', registered_subject=options.get('registered_subject'))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        self.maternal_visit = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')

        mommy.make_recipe('td_maternal.maternallabourdel', registered_subject=self.registered_subject)

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2000M')
        mommy.make_recipe('td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='2010M')
        self.maternal_visit_2000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=self.appointment, reason='scheduled')

        contraceptives = Contraceptives.objects.create(
            hostname_created="django", name="Condom", short_name="Condom", created=timezone.datetime.now(), 
            user_modified="", modified=timezone.datetime.now(), hostname_modified="django", version="1.0", 
            display_index=1, user_created="django", field_name=None, revision=":develop:")

        maternal_relatives = MaternalRelatives.objects.create(
            hostname_created="django", name="Mother", short_name="Mother", created=timezone.datetime.now(), 
            user_modified="", modified=timezone.datetime.now(), hostname_modified="django", version="1.0", 
            display_index=1, user_created="django", field_name=None, revision=":develop:")

        self.options = {
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit.id,
            'more_children': YES,
            'next_child': 'between 2-5years from now',
            'contraceptive_measure': YES,
            'contraceptive_partner': YES,
            'contraceptive_relative': [maternal_relatives.id],
            'influential_decision_making': 'partner_most_influential',
            'uses_contraceptive': YES,
            'contraceptive_startdate': date.today(),
            'contr': [contraceptives.id],
            'another_pregnancy': YES,
            'pregnancy_date': date.today(),
            'pap_smear': YES,
            'pap_smear_date': date.today(),
            'pap_smear_estimate': 'within_last_6months',
            'pap_smear_result': YES,
            'pap_smear_result_status': 'normal',
            'pap_smear_result_abnormal': None,
            'srh_referral': YES}

    def test_more_children(self):
        self.options['more_children'] = NO
        self.options['next_child'] = 'between 2-5years from now'
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'You said the client does not desire more children please do not answer '
            'When would you like to have your next child?',
            form.errors.get('__all__'))

    def test_next_none(self):
        self.options['more_children'] = YES
        self.options['next_child'] = None
        self.options['contraceptive_measure'] = YES
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant desires more children, question on next child cannot be None.',
            form.errors.get('__all__'))

    def test_uses_contraceptive_yes(self):
        self.options['more_children'] = YES
        self.options['uses_contraceptive'] = YES
        self.options['contr'] = None
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant uses a contraceptive method, please select a valid method',
            form.errors.get('__all__'))

    def test_uses_contraceptive_no(self):
        self.options['more_children'] = YES
        self.options['uses_contraceptive'] = NO
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant does not use a contraceptive method, no need to give a contraceptive method',
            form.errors.get('__all__'))

    def test_pap_smear_yes(self):
        self.options['pap_smear'] = YES
        self.options['pap_smear_date'] = None
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn('Please give the date the pap smear was done.', form.errors.get('__all__'))

    def test_pap_smear_no(self):
        self.options['pap_smear'] = NO
        self.options['pap_smear_date'] = date.today()
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Pap smear date not known, please do not add it.',
            form.errors.get('__all__'))

    def test_pap_smear_result_yes(self):
        self.options['pap_smear'] = YES
        self.options['pap_smear_date'] = date.today()
        self.options['pap_smear_result'] = YES
        self.options['pap_smear_result_status'] = None
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant knows her pap smear result, please give the status of the pap smear.',
            form.errors.get('__all__'))

    def test_pap_smear_result_no(self):
        self.options['pap_smear'] = YES
        self.options['pap_smear_date'] = date.today()
        self.options['pap_smear_result'] = NO
        self.options['pap_smear_result_status'] = 'abnormal'
        self.options['pap_smear_result_abnormal'] = 'Yeast Infection'
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant pap smear result not known, no need to give pap smear status or notification date.',
            form.errors.get('__all__'))

    def test_pap_smear_date_estimate(self):
        self.options['pap_smear'] = YES
        self.options['pap_smear_date'] = date.today()
        self.options['pap_smear_estimate'] = None
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Pap smear date has been provided, please let us know if this date has been estimated.',
            form.errors.get('__all__'))

    def test_no_contraceptive_startdate(self):
        self.options['contraceptive_startdate'] = None
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant uses a contraceptive method, please give a contraceptive startdate.',
            form.errors.get('__all__'))

    def test_another_pregnancy_yes(self):
        self.options['pregnancy_date'] = None
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant is pregnant, please give date participant found out.',
            form.errors.get('__all__'))

    def test_another_pregnancy_no(self):
        self.options['pregnancy_date'] = None
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant is pregnant, please give date participant found out.',
            form.errors.get('__all__'))
