from datetime import date
from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from td_list.models import Contraceptives, MaternalRelatives

from ..forms import MaternalContraceptionForm

from .test_mixins import PosMotherMixin


class TestMaternalContraceptionForm(PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalContraceptionForm, self).setUp()

        self.complete_required_crfs('1000M')
        self.make_antenatal_enrollment_two()
        self.complete_required_crfs('1010M', '1020M')
        self.make_delivery()
        self.complete_required_crfs('2000M')
        maternal_visit = self.add_maternal_visit('2010M')

        contraceptives = Contraceptives.objects.create(
            hostname_created="django", name="Condom", short_name="Condom", created=get_utcnow(),
            user_modified="", modified=get_utcnow(), hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None, revision=":develop:")

        maternal_relatives = MaternalRelatives.objects.create(
            hostname_created="django", name="Mother", short_name="Mother", created=get_utcnow(),
            user_modified="", modified=get_utcnow(), hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None, revision=":develop:")

        self.options = {
            'maternal_visit': maternal_visit.id,
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
        self.options.update(
            more_children=NO,
            next_child='between 2-5years from now')
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'You said the client does not desire more children please do not answer '
            'When would you like to have your next child?',
            form.errors.get('__all__'))

    def test_next_none(self):
        self.options.update(
            more_children=YES,
            next_child=None,
            contraceptive_measure=YES)
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant desires more children, question on next child cannot be None.',
            form.errors.get('__all__'))

    def test_uses_contraceptive_yes(self):
        self.options.update(
            more_children=YES,
            uses_contraceptive=YES,
            contr=None)
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant uses a contraceptive method, please select a valid method',
            form.errors.get('__all__'))

    def test_uses_contraceptive_no(self):
        self.options.update(
            more_children=YES,
            uses_contraceptive=NO)
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant does not use a contraceptive method, no need to give a contraceptive method',
            form.errors.get('__all__'))

    def test_pap_smear_yes(self):
        self.options.update(
            pap_smear=YES,
            pap_smear_date=None)
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn('Please give the date the pap smear was done.', form.errors.get('__all__'))

    def test_pap_smear_no(self):
        self.options.update(
            pap_smear=NO,
            pap_smear_date=get_utcnow().date())
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Pap smear date not known, please do not add it.',
            form.errors.get('__all__'))

    def test_pap_smear_result_yes(self):
        self.options.update(
            pap_smear=YES,
            pap_smear_date=get_utcnow().date(),
            pap_smear_result=YES,
            pap_smear_result_status=None)
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant knows her pap smear result, please give the status of the pap smear.',
            form.errors.get('__all__'))

    def test_pap_smear_result_no(self):
        self.options.update(
            pap_smear=YES,
            pap_smear_date=get_utcnow().date(),
            pap_smear_result=NO,
            pap_smear_result_status='abnormal',
            pap_smear_result_abnormal='Yeast Infection')
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant pap smear result not known, no need to give pap smear status or notification date.',
            form.errors.get('__all__'))

    def test_pap_smear_date_estimate(self):
        self.options.update(
            pap_smear=YES,
            pap_smear_date=get_utcnow().date(),
            pap_smear_estimate=None)
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Pap smear date has been provided, please let us know if this date has been estimated.',
            form.errors.get('__all__'))

    def test_no_contraceptive_startdate(self):
        self.options.update(contraceptive_startdate=None)
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant uses a contraceptive method, please give a contraceptive startdate.',
            form.errors.get('__all__'))

    def test_another_pregnancy_yes(self):
        self.options.update(pregnancy_date=None)
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant is pregnant, please give date participant found out.',
            form.errors.get('__all__'))

    def test_another_pregnancy_no(self):
        self.options.update(pregnancy_date=None)
        form = MaternalContraceptionForm(data=self.options)
        self.assertIn(
            'Participant is pregnant, please give date participant found out.',
            form.errors.get('__all__'))
