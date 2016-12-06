from model_mommy import mommy

from td.models import Appointment
from edc_visit_tracking.constants import SCHEDULED


import os

from unipath import Path

from td_list.models import RandomizationItem


def load_test_randomization():
    """Loads a test randomization CSV and adds data to RandomizationItem model."""
    f = open(os.path.join(
             Path(os.path.dirname(os.path.realpath(__file__))), 'test_randomization.csv'))
    for index, line in enumerate(f.readlines()):
        if index == 0:
            continue
        seq, drug_assignment = line.split(',')
        RandomizationItem.objects.get_or_create(name=seq, field_name=drug_assignment)


class PosMotherMixin:
    """Creates a POS mother."""
    def setUp(self):
        super(PosMotherMixin, self).setUp()
        load_test_randomization()
        self.study_site = '40'
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent',
            maternal_eligibility_reference=self.maternal_eligibility.reference_pk)
        self.subject_identifier = self.maternal_consent.subject_identifier
        self.antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment_pos',
            subject_identifier=self.subject_identifier)
        self.appointment_1000 = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code='1000M')
        self.maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit',
            appointment=self.appointment_1000,
            reason=SCHEDULED)
        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=self.maternal_visit_1000,
            number_of_gestations=1)
        self.antenatal_enrollment_two = mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo',
            subject_identifier=self.subject_identifier)
        self.appointment_1010M = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code='1010M')
        self.antenatal_visit_1 = mommy.make_recipe(
            'td_maternal.maternalvisit',
            appointment=self.appointment_1010M, reason='scheduled')


class NegMotherMixin:
    """Creates a NEG mother and visits up to 1010M."""
    def setUp(self):
        pass
