from model_mommy import mommy

from td_list.list_data import list_data
from edc_constants.constants import YES, NEG
from td_maternal.tests.test_mixins import MotherMixin, AddMaternalVisitMixin


class AddInfantVisitMixin(AddMaternalVisitMixin):

    infant_model_label = 'td_infant.infantvisit'

    def add_infant_visit(self, visit_code, reason=None):
        return self.add_visit(self.infant_model_label, visit_code, reason)

    def add_infant_visits(self, *visit_codes):
        return self.add_visits(self.infant_model_label, *visit_codes)

    def get_infant_visit(self, visit_code):
        return self.get_visit(self.infant_model_label, visit_code)

    def get_last_infant_visit(self):
        return self.get_last_visit(self.infant_model_label)


class CompleteInfantCrfsMixin(MotherMixin):

    def complete_required_infant_crfs(self, *visit_codes):
        """Complete all required CRFs for a visit(s) using mommy defaults."""
        complete_required_crfs = {}
        for visit_code in visit_codes:
            infant_visit = self.add_infant_visit(visit_code)
            completed_crfs = super(CompleteInfantCrfsMixin, self).complete_required_crfs(
                visit_code, infant_visit, 'infant_visit')
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

    def make_infant_birth_arv(self, infant_visit=None, **options):
        infant_visit = infant_visit or self.get_last_infant_visit()
        azt_discharge_supply = options.get('azt_discharge_supply', YES)
        options.update(azt_discharge_supply=azt_discharge_supply)
        self.infant_birth_arv = mommy.make_recipe(
            'td_infant.infantbirtharv',
            infant_visit=infant_visit,
            **options)

    def make_infantarvproph(self, infant_visit=None, **options):
        infant_visit = infant_visit or self.get_last_infant_visit()
        arv_status = options.get('arv_status', YES)
        options.update(arv_status=arv_status)
        self.infantarvproph = mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=infant_visit,
            arv_status=arv_status)
