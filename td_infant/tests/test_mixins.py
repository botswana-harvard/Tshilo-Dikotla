from model_mommy import mommy
from edc_base.test_mixins import AddVisitMixin


class AddVisitInfantMixin(AddVisitMixin):

    infant_model_label = 'td_infant.infantvisit'

    def add_infant_visit(self, code, reason=None):
        return self.add_visit(self.infant_model_label, code, reason)

    def add_infant_visits(self, *codes):
        self.add_visits(self.infant_model_label, *codes)

    def get_infant_visit(self, code):
        return self.get_visit(self.infant_model_label, code)


class InfantBirthMixin:
    """Adds the infant birth model."""
    def setUp(self):
        super(InfantBirthMixin, self).setUp()
        self.infant_birth = mommy.make_recipe(
            'td_infant.infantbirth',
            delivery_reference=self.maternal_lab_del.reference,
            birth_order=1,
            birth_order_denominator=1)
