from model_mommy import mommy

from django.apps import apps as django_apps
from td.models import Appointment


import os

from unipath import Path

from td_list.models import RandomizationItem


class TestMixinError(Exception):
    pass


def load_test_randomization():
    """Loads a test randomization CSV and adds data to RandomizationItem model."""
    f = open(os.path.join(
             Path(os.path.dirname(os.path.realpath(__file__))), 'test_randomization.csv'))
    for index, line in enumerate(f.readlines()):
        if index == 0:
            continue
        seq, drug_assignment = line.split(',')
        RandomizationItem.objects.get_or_create(name=seq, field_name=drug_assignment)


class AddVisitMixin:

    def add_visit(self, model_label, code, reason=None):
        """Adds (or gets) and returns a visit for give model and code."""
        reason = reason or 'scheduled'
        model = django_apps.get_model(*model_label.split('.'))
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code=code)
        try:
            visit = self.get_visit(model_label, code)
        except model.DoesNotExist:
            visit = mommy.make_recipe(
                model_label,
                appointment=appointment, reason=reason)
        return visit

    def add_visits(self, model_label, *codes):
        """Adds a sequence of visits for the codes provided.

        If a infant visit already exists, it will just pass."""
        for code in codes:
            self.add_visit(model_label, code)

    def get_visit(self, model_label, code):
        """Returns a visit instance if it exists."""
        model = django_apps.get_model(*model_label.split('.'))
        return model.objects.get(
            appointment__subject_identifier=self.subject_identifier, visit_code=code)


class AddVisitInfantMixin(AddVisitMixin):

    infant_model_label = 'td_infant.infantvisit'

    def add_infant_visit(self, code, reason=None):
        return self.add_visit(self.infant_model_label, code, reason)

    def add_infant_visits(self, *codes):
        self.add_visits(self.infant_model_label, *codes)

    def get_infant_visit(self, code):
        return self.get_visit(self.infant_model_label, code)


class AddVisitMotherMixin(AddVisitMixin):

    maternal_model_label = 'td_maternal.maternalvisit'

    def add_maternal_visit(self, code, reason=None):
        return self.add_visit(self.maternal_model_label, code, reason)

    def add_maternal_visits(self, *codes):
        self.add_visits(self.maternal_model_label, *codes)

    def get_maternal_visit(self, code):
        return self.get_visit(self.maternal_model_label, code)


class MotherMixin():
    """Creates a POS mother."""
    def setUp(self):
        super(MotherMixin, self).setUp()
        load_test_randomization()
        self.study_site = '40'
        self.maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        self.maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent',
            maternal_eligibility_reference=self.maternal_eligibility.reference_pk)
        self.subject_identifier = self.maternal_consent.subject_identifier


class PosMotherMixin(MotherMixin):
    """Creates a POS mother."""
    def setUp(self):
        super(PosMotherMixin, self).setUp()
        self.antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment_pos',
            subject_identifier=self.subject_identifier)


class NegMotherMixin(MotherMixin):
    """Creates a NEG mother and visits up to 1010M."""
    def setUp(self):
        super(NegMotherMixin, self).setUp()
        self.antenatal_enrollment = mommy.make_recipe(
            'td_maternal.antenatalenrollment_neg',
            subject_identifier=self.subject_identifier)


class AntenatalVisitsMotherMixin(AddVisitMotherMixin):
    """Adds ultrasound, enrollmenttwo and visits up to 1010 for any mother."""
    def setUp(self):
        super(AntenatalVisitsMotherMixin, self).setUp()
        try:
            self.antenatal_enrollment
        except AttributeError as e:
            raise TestMixinError(
                'TestCase Mixin requires a POS/NEGMotherMixin that completes antenatal_enrollment. '
                'Got {}'.format(str(e)))
        maternal_visit = self.add_maternal_visit('1000M')
        self.maternal_ultrasound = mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial',
            maternal_visit=maternal_visit,
            number_of_gestations=1)
        self.antenatal_enrollment_two = mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo',
            subject_identifier=self.subject_identifier)
        self.add_maternal_visit('1010M')


class DeliverMotherMixin:
    """Adds the delivery and birth model."""
    def setUp(self):
        super(DeliverMotherMixin, self).setUp()
        self.maternal_lab_del = mommy.make_recipe(
            'td_maternal.maternallabdel',
            subject_identifier=self.subject_identifier,
            live_infants=1)
        self.infant_birth = mommy.make_recipe(
            'td_infant.infantbirth',
            delivery_reference=self.maternal_lab_del.reference,
            birth_order=1,
            birth_order_denominator=1)
