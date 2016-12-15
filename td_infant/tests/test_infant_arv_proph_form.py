from django.test import TestCase, tag
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, UNKNOWN, POS, NEW

from td.constants import MODIFIED, DISCONTINUED, NEVER_STARTED

from ..forms import InfantArvProphForm, InfantArvProphModForm

from .test_mixins import InfantMixin


@tag('me')
class TestInfantArvProph(InfantMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010')

    def test_validate_taking_arv_proph_no(self):
        """Assert InfantArvProphForm is invalid if the infant was not taking prophylactic arv
        and arv_status is not Not Applicable."""
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=NO)
        data = dict(
            prophylatic_nvp=NO,
            arv_status=MODIFIED,
            infant_visit=self.get_infant_visit('2010').id)
        form = InfantArvProphForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(u'Infant was not taking prophylactic arv, prophylaxis should be Never Started or Discontinued.',
                      form.errors.get('__all__'))

    def test_validate_taking_arv_proph_discontinued(self):
        """Assert InfantArvProphForm is invalid if arv_status is discontinued."""
        # not given ARVs at discharge 2000
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=UNKNOWN)
        # should not be able to say DISCONTINUED at 2010 
        data = dict(
            infant_visit=self.get_infant_visit('2010').id,
            prophylatic_nvp=NO,
            arv_status=DISCONTINUED)
        form = InfantArvProphForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            u'The azt discharge supply in Infant birth arv was answered as NO or Unknown, '
            'therefore Infant ARV proph in this visit cannot be permanently discontinued.',
            form.errors.get('__all__'))

    def test_validate_taking_arv_proph_yes(self):
        """Assert InfantArvProphForm is invalid if the infant was not taking prophylactic arv and
        arv_status is Never Started"""
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=YES)
        data = dict(
            infant_visit=self.get_infant_visit('2010').id,
            report_datetime=get_utcnow(),
            prophylatic_nvp=YES,
            arv_status=NEVER_STARTED)
        form = InfantArvProphForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Infant has been on prophylactic arv, cannot choose Never Started or Permanently discontinued.',
            form.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_dose_status(self):
        """Assert InfantArvProphForm is invalid if arv_code is given but dose_status is none."""
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=YES)
        infant_arv_proph = mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=self.get_infant_visit('2010'),
            arv_status=YES)
        data = dict(
            infant_arv_proph=infant_arv_proph.id,
            arv_code='Nevirapine',
            dose_status=None,
            modification_date=get_utcnow().date(),
            modification_code='Initial dose')
        form = InfantArvProphModForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(u'You entered an ARV Code, please give the dose status.',
                      form.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_date(self):
        """Assert InfantArvProphForm is invalid if arv_code is given but modification_date is none."""
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=YES)
        infant_arv_proph = mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=self.get_infant_visit('2010'),
            arv_status=YES)
        data = {'infant_arv_proph': infant_arv_proph.id,
                'arv_code': 'Nevirapine',
                'dose_status': NEW,
                'modification_date': None,
                'modification_code': 'Initial dose'}
        form = InfantArvProphModForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'You entered an ARV Code, please give the modification date.',
            form.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_code(self):
        """Assert InfantArvProphForm is invalid if arv_code is given but modification_code is none."""
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=YES)
        infant_arv_proph = mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=self.get_infant_visit('2010'),
            arv_status=YES)
        data = {'infant_arv_proph': infant_arv_proph.id,
                'arv_code': 'Nevirapine',
                'dose_status': NEW,
                'modification_date': get_utcnow().date(),
                'modification_code': None}
        form = InfantArvProphModForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'You entered an ARV Code, please give the modification reason.',
            form.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_not_needed(self):
        """Assert InfantArvProphForm is invalid if inline is completed with arv_status not in modified."""
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=YES)
        infant_arv_proph = mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=self.get_infant_visit('2010'),
            arv_status=YES)
        data = {'infant_arv_proph': infant_arv_proph.id,
                'arv_code': 'Nevirapine',
                'dose_status': NEW,
                'modification_date': get_utcnow().date(),
                'modification_code': 'Initial dose'}
        form = InfantArvProphModForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(u'You did NOT indicate that medication was modified, so do not ENTER arv inline.',
                      form.errors.get('__all__'))

    def test_validate_infant_arv_azt_initiated(self):
        """Assert that the azt dose is not initiated more than once."""
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=YES)
        infant_arv_proph = mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=self.get_infant_visit('2010'),
            arv_status=MODIFIED)
        data = {'infant_arv_proph': infant_arv_proph.id,
                'arv_code': 'Zidovudine',
                'dose_status': NEW,
                'modification_date': get_utcnow().date(),
                'modification_code': 'Initial dose'}
        form = InfantArvProphModForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            u'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
            'AZT cannot be initiated again.',
            form.errors.get('__all__'))

    def test_validate_infant_arv_azt_different(self):
        """Assert that the dose being modified is the same one infant was discharged with."""
        mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=self.get_infant_visit('2000'),
            azt_discharge_supply=YES)
        infant_arv_proph = mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=self.get_infant_visit('2010'),
            arv_status=MODIFIED)
        data = {'infant_arv_proph': infant_arv_proph.id,
                'arv_code': 'Nevarapine',
                'dose_status': NEW,
                'modification_date': get_utcnow().date(),
                'modification_code': 'Initial dose'}
        form = InfantArvProphModForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            u'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
            'Arv Code should be AZT',
            form.errors.get('__all__'))
