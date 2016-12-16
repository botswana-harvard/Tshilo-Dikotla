from model_mommy import mommy

from edc_constants.constants import NEG

from td_list.list_data import list_data
from td_maternal.tests.test_mixins import MotherMixin, AddMaternalVisitMixin


class AddInfantVisitMixin(AddMaternalVisitMixin):

    infant_model_label = 'td_infant.infantvisit'

    def add_infant_visit(self, visit_code=None, reason=None):
        return self.add_visit(
            visit_code=visit_code,
            model_label=self.infant_model_label,
            reason=reason,
            subject_identifier=self.infant_identifier)

    def add_infant_visits(self, *visit_codes, reason=None):
        return self.add_visits(
            *visit_codes,
            model_label=self.infant_model_label,
            subject_identifier=self.infant_identifier,
            reason=reason)

    def get_infant_visit(self, visit_code):
        return self.get_visit(
            visit_code=visit_code,
            model_label=self.infant_model_label,
            subject_identifier=self.infant_identifier)

    def get_last_infant_visit(self):
        return self.get_last_visit(
            model_label=self.infant_model_label,
            subject_identifier=self.infant_identifier)


class CompleteInfantCrfsMixin(MotherMixin):

    def complete_required_infant_crfs(self, *visit_codes):
        """Complete all required CRFs for a visit(s) using mommy defaults."""
        complete_required_crfs = {}
        for visit_code in visit_codes:
            infant_visit = self.add_infant_visit(visit_code)
            completed_crfs = super(CompleteInfantCrfsMixin, self).complete_required_crfs(
                visit_code=visit_code,
                visit=infant_visit,
                visit_attr='infant_visit',
                subject_identifier=self.infant_identifier)
            complete_required_crfs.update({visit_code: completed_crfs})
        return complete_required_crfs


class InfantTestMixin(CompleteInfantCrfsMixin, AddInfantVisitMixin):

    list_data = list_data


class InfantMixin(InfantTestMixin):
    def setUp(self):
        super(InfantMixin, self).setUp()
        self.study_site = '40'

    def make_positive_mother_and_deliver(self):
        super(InfantMixin, self).make_positive_mother()
        self.add_maternal_visit('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        self.maternal_lab_del = self.make_delivery()
        return self.maternal_lab_del.reference

    def make_negative_mother_and_deliver(self):
        super(InfantMixin, self).make_negative_mother()
        self.add_maternal_visit('1000M')
        self.make_antenatal_enrollment_two()
        self.add_maternal_visits('1010M', '1020M')
        self.maternal_lab_del = self.make_delivery()
        return self.maternal_lab_del.reference

    def make_infant_birth(self, maternal_status=None, birth_order=None, birth_order_denominator=None, **options):
        """Completes the infant birth and all maternal visits and delivery required to that point."""
        if maternal_status == NEG:
            delivery_reference = self.make_negative_mother_and_deliver()
        else:
            delivery_reference = self.make_positive_mother_and_deliver()
        birth_order = birth_order or 1
        birth_order_denominator = birth_order_denominator or 1
        self.infant_birth = mommy.make_recipe(
            'td_infant.infantbirth',
            report_datetime=self.maternal_lab_del.report_datetime,
            delivery_reference=delivery_reference,
            dob=self.maternal_lab_del.delivery_datetime.date(),
            birth_order=1,
            birth_order_denominator=1,
            **options)
        self.infant_identifier = self.infant_birth.subject_identifier
