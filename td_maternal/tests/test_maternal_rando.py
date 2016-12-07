from django.test.testcases import TestCase
from django.utils import timezone
from model_mommy import mommy

from edc_constants.constants import YES

from td.models import Appointment

from .mixins import NegMotherMixin, PosMotherMixin, AntenatalVisitsMotherMixin
from td_maternal.forms import MaternalRandoForm


class TestMaternalRandomizationForm(AntenatalVisitsMotherMixin, NegMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalRandomizationForm, self).setUp()

    def test_pos_mother_validation(self):
        options = {
            'maternal_visit': self.get_maternal_visit('1000M').id,
            'site': 'gaborone',
            'sid': 1,
            'randomization_datetime': timezone.now(),
            'initials': 'CT',
            'dispensed': YES,
            'delivery_clinic': 'PMH'
        }
        form = MaternalRandoForm(data=options)
        self.assertIn('Mother must be HIV(+) to randomize.', form.errors.get('__all__'))


class TestMaternalRandomization(AntenatalVisitsMotherMixin, PosMotherMixin, TestCase):

    def setUp(self):
        super(TestMaternalRandomization, self).setUp()

    def test_pick_correct_next_randomization_item(self):
        """Test if the next correct randomization item is picked."""
        maternal_rando = mommy.make_recipe('td_maternal.maternalrando', maternal_visit=self.get_maternal_visit('1010M'))
        self.assertEqual(maternal_rando.sid, 1)

        # Create another mother
        maternal_eligibility_2 = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent_2 = mommy.make_recipe(
            'td_maternal.maternalconsent',
            maternal_eligibility_reference=maternal_eligibility_2.reference_pk)
        mommy.make_recipe('td_maternal.antenatalenrollment_pos', subject_identifier=maternal_consent_2.subject_identifier)
        appointment = Appointment.objects.get(
            subject_identifier=maternal_consent_2.subject_identifier, visit_code='1000M')
        maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=appointment, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=maternal_visit_1000, number_of_gestations=1)
        mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo',
            subject_identifier=maternal_consent_2.subject_identifier)

        appointment_2 = Appointment.objects.get(
            subject_identifier=maternal_consent_2.subject_identifier, visit_code='1010M')
        maternal_visit_1010 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=appointment_2, reason='scheduled')
        maternal_rando_2 = mommy.make_recipe('td_maternal.maternalrando', maternal_visit=maternal_visit_1010)
        self.assertEqual(maternal_rando_2.sid, 2)
