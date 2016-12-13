from datetime import date
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NO

from ..forms import VaccinesReceivedForm, VaccinesMissedForm
from .test_mixins import InfantMixin


class TestInfantImmunizationForm(InfantMixin, TestCase):

    def setUp(self):
        super(TestInfantImmunizationForm, self).setUp()
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010', '2020')
        self.infant_visit = self.get_infant_visit('2020')

        self.options = {
            'report_datetime': get_utcnow(),
            'infant_visit': self.infant_visit,
            'vaccines_received': YES,
            'vaccines_missed': NO
        }

    def test_vaccines_received_no_table_filling(self):
        """Assert a validation message is raised when an infant that received vaccines
        but received vaccines table not filled."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': None,
                           'date_given': None,
                           'infant_age': None}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("You mentioned that vaccines where received. Please"
                      " indicate which ones on the Received Vaccines table.",
                      vaccine_received_form.errors.get('__all__'))

    def test_vaccines_not_received_table_filled(self):
        """Assert a validation message is raised when an infant that did not
        receive vaccines but received vaccines table is filled."""
        self.options = {
            'report_datetime': get_utcnow(),
            'infant_visit': self.infant_visit,
            'vaccines_received': NO,
            'vaccines_missed': NO
        }
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'Hepatitis_B',
                           'date_given': date.today(),
                           'infant_age': '2'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("No vaccines received. Do not fill Received Vaccines table",
                      vaccine_received_form.errors.get('__all__'))

    def test_vaccines_missed_no_table_filling(self):
        """Assert a validation message is raised when an infant that missed
        vaccines and missed vaccine table not filled."""
        self.options = {
            'report_datetime': get_utcnow(),
            'infant_visit': self.infant_visit,
            'vaccines_received': NO,
            'vaccines_missed': YES
        }
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'missed_vaccine_name': None,
                           'reason_missed': None,
                           'reason_missed_other': None}
        vaccine_missed_form = VaccinesMissedForm(data=received_inline)
        self.assertIn("You mentioned that the child missed some vaccines."
                      " Please indicate which ones in the Missed Vaccines "
                      "table.", vaccine_missed_form.errors.get('__all__'))

    def test_vaccines_not_missed_table_filled(self):
        """Assert a validation message is raised when an infant that did not miss
        vaccines and missed vaccine table is filled filled."""
        self.options = {
            'report_datetime': get_utcnow(),
            'infant_visit': self.infant_visit,
            'vaccines_received': NO,
            'vaccines_missed': NO
        }
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'missed_vaccine_name': 'Vitamin_A',
                           'reason_missed': 'Was not in country',
                           'reason_missed_other': None}
        vaccine_missed_form = VaccinesMissedForm(data=received_inline)
        self.assertIn("No vaccines missed. Do not fill Missed Vaccines table",
                      vaccine_missed_form.errors.get('__all__'))

    def test_missed_vaccine_fields(self):
        """Assert that when a missed vaccine name is given that the reason should be provided."""
        self.options = {
            'report_datetime': get_utcnow(),
            'infant_visit': self.infant_visit,
            'vaccines_received': NO,
            'vaccines_missed': YES
        }
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'missed_vaccine_name': 'BCG',
                           'reason_missed': None,
                           'reason_missed_other': None}
        vaccine_missed_form = VaccinesMissedForm(data=received_inline)
        self.assertIn("You said {} vaccine was missed. Give a reason for missing this"
                      " vaccine".format(received_inline['missed_vaccine_name']), vaccine_missed_form.errors.get('__all__'))

    def test_vaccine_received_date_not_less_than_birth(self):
        """Assert that the vaccine date is not less than the birth date."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'BCG',
                           'date_given': (get_utcnow() - relativedelta(years=37)).date(),
                           'infant_age': 'At Birth'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("Vaccine date cannot be before infant date of birth. ",
                      vaccine_received_form.errors.get('__all__'))

    def test_received_vaccine_fields_date(self):
        """Assert that when a receive vaccine name is filled that a date is provided."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'BCG',
                           'date_given': None,
                           'infant_age': 'At Birth'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("You provided a vaccine name {}. What date was it given to the "
                      "infant?".format(received_inline['received_vaccine_name']), vaccine_received_form.errors.get('__all__'))

    def test_received_vaccine_fields_age(self):
        """Assert that when a receive vaccine name is filled that the age in months
        the vaccine was givne to the infant is provided."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'BCG',
                           'date_given': (timezone.datetime.now() - relativedelta(weeks=37)).date(),
                           'infant_age': None}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("You provided a vaccine name {}. At how many months "
                      "was it given to the infant?".format(received_inline['received_vaccine_name']), vaccine_received_form.errors.get('__all__'))

    def test_received_vaccination_at_birth_bcg(self):
        """Assert that the correct vaccine is given at birth or few days after birth."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'BCG',
                           'date_given': date.today(),
                           'infant_age': '2'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("BCG vaccination is ONLY given at birth or few days after birth",
                      vaccine_received_form.errors.get('__all__'))

    def test_received_hepatitis_vaccine(self):
        """Assert that the hepatitis vaccine is not given at inappropriate infant age."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'Hepatitis_B',
                           'date_given': date.today(),
                           'infant_age': '6-11'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("Hepatitis B can only be administered at birth or 2 or 3 or 4 "
                      "months of infant life", vaccine_received_form.errors.get('__all__'))

    def test_receievd_dpt_vaccine(self):
        """Assert that DPT vaccine is not given at inappropriate infant age."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'DPT',
                           'date_given': date.today(),
                           'infant_age': '6-11'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("DPT. Diphtheria, Pertussis and Tetanus can only be administered at"
                      " 2 or 3 or 4 months ONLY.", vaccine_received_form.errors.get('__all__'))

    def test_received_haemophilus_vaccine(self):
        """Assert that haemophilus influenza vaccine is not administered at inappropiate infant age."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'Haemophilus_influenza',
                           'date_given': date.today(),
                           'infant_age': '6-11'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("Haemophilus Influenza B vaccine can only be given at 2 or 3 or"
                      " 4 months of infant life.", vaccine_received_form.errors.get('__all__'))

    def test_received_pcv_vaccine(self):
        """Assert that PCV is administered at correct age."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'PCV_Vaccine',
                           'date_given': date.today(),
                           'infant_age': '6-11'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("The PCV [Pneumonia Conjugated Vaccine], can ONLY be administered at"
                      " 2 or 3 or 4 months of infant life.", vaccine_received_form.errors.get('__all__'))

    def test_received_polio_vaccine(self):
        """Assert that polio vaccine is administered at correct age."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'Polio',
                           'date_given': date.today(),
                           'infant_age': '6-11'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("Polio vaccine can only be administered at 2 or 3 or 4 or 18 "
                      "months of infant life", vaccine_received_form.errors.get('__all__'))

    def test_received_rotavirus_vaccine(self):
        """Assert rotavirus administered to infant at age 4months."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'Rotavirus',
                           'date_given': date.today(),
                           'infant_age': '4'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("Rotavirus is only administered at 2 or 3 months of"
                      " infant life", vaccine_received_form.errors.get('__all__'))

    def test_received_measles_vaccine(self):
        """Assert measles vaccine administered to an infant who is only a month old."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'Measles',
                           'date_given': date.today(),
                           'infant_age': '2'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("Measles vaccine is only administered at 9 or 18"
                      " months of infant life.", vaccine_received_form.errors.get('__all__'))

    def test_received_pentavalent_vaccine(self):
        """Assert for Pentavalent vaccine administered at 6-11 months of infant life."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'Pentavalent',
                           'date_given': date.today(),
                           'infant_age': '6-11'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("The Pentavalent vaccine can only be administered at 2 or 3 or"
                      " 4 months of infant life.", vaccine_received_form.errors.get('__all__'))

    def test_received_vitamin_a_vaccine(self):
        """Assert for Vitamin A vaccine administered earlier than 6 months."""
        infant_fu_immunizations = mommy.make_recipe(
            'td_infant.infantimmunizations', **self.options)
        received_inline = {'infant_fu_immunizations': infant_fu_immunizations.id,
                           'received_vaccine_name': 'Vitamin_A',
                           'date_given': date.today(),
                           'infant_age': '2'}
        vaccine_received_form = VaccinesReceivedForm(data=received_inline)
        self.assertIn("Vitamin A is given to children between 6-11 months of"
                      " life", vaccine_received_form.errors.get('__all__'))
