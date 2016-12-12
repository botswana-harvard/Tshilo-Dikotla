from datetime import date
from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, UNKNOWN

from td.constants import MODIFIED, DISCONTINUED, NEVER_STARTED

from ..forms import InfantArvProphForm, InfantArvProphModForm

from td_maternal.tests.test_mixins import MotherMixin
from .test_mixins import AddVisitInfantMixin, InfantBirthMixin


class TestInfantArvProph(AddVisitInfantMixin, InfantBirthMixin, MotherMixin, TestCase):

    def setUp(self):
        super(TestInfantArvProph, self).setUp()
        self.make_positive_mother()
        self.add_maternal_visit('1000M')
        self.make_ultrasound(self.get_maternal_visit('1000M'))
        self.make_antenatal_enrollment_two()
        self.add_maternal_visit('1010M')
        self.add_maternal_visit('1020M')
        self.make_delivery()
        self.add_maternal_visit('2000M')
        self.add_infant_visit('2000M')
        self.make_infant_birth()
        self.make_infant_birth_arv(self.get_infant_visit('2000M'))
        self.add_infant_visit('2010M')
        self.make_infant_arv_proph(self.get_infant_visit('2010M'))

        self.data = {
            'infant_visit': self.get_infant_visit('2010M').id,
            'report_datetime': get_utcnow(),
            'prophylatic_nvp': YES,
            'arv_status': MODIFIED,
        }

    def test_validate_taking_arv_proph_no(self):
        """Test if the infant was not taking prophylactic arv and arv status is not Not Applicable"""
        self.data.update(
            prophylatic_nvp=NO,
            arv_status=MODIFIED)
        infant_arv_proph = InfantArvProphForm(data=self.data)

        self.assertIn(u'Infant was not taking prophylactic arv, prophylaxis should be Never Started or Discontinued.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_taking_arv_proph_discontinued(self):
        """Test if the was not taking  prophylactic arv and infant was not given arv's at birth"""
        self.infant_birth_arv.azt_discharge_supply = UNKNOWN
        self.infant_birth_arv.save()
        self.data.update(
            prophylatic_nvp=NO,
            arv_status=DISCONTINUED)
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(
            u'The azt discharge supply in Infant birth arv was answered as NO or Unknown, '
            'therefore Infant ARV proph in this visit cannot be permanently discontinued.',
            infant_arv_proph.errors.get('__all__'))

    def test_validate_taking_arv_proph_yes(self):
        """Test if the infant was not taking prophylactic arv and arv status is Never Started"""
        self.data.update(
            prophylatic_nvp=YES,
            arv_status=NEVER_STARTED)
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(u'Infant has been on prophylactic arv, cannot choose Never Started or Permanently discontinued.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_dose_status(self):
        inline_data = {'infant_arv_proph': self.infantarvproph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': None,
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You entered an ARV Code, please give the dose status.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_date(self):
        inline_data = {'infant_arv_proph': self.infantarvproph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': 'New',
                       'modification_date': None,
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You entered an ARV Code, please give the modification date.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_code(self):
        inline_data = {'infant_arv_proph': self.infantarvproph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': None}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You entered an ARV Code, please give the modification reason.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_not_needed(self):
        inline_data = {'infant_arv_proph': self.infantarvproph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You did NOT indicate that medication was modified, so do not ENTER arv inline.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_azt_initiated(self):
        """Check that the azt dose is not initiated more than once"""
        self.infant_birth_arv.azt_discharge_supply = YES
        self.infant_birth_arv.save()
        inline_data = {'infant_arv_proph': self.infantarvproph.id,
                       'arv_code': 'Zidovudine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(
            u'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
            'AZT cannot be initiated again.',
            infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_azt_different(self):
        """Check that the dose being modified is the same one infant was discharged with."""
        inline_data = {'infant_arv_proph': self.infantarvproph.id,
                       'arv_code': 'Nevarapine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(
            u'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
            'Arv Code should be AZT',
            infant_arv_proph.errors.get('__all__'))
