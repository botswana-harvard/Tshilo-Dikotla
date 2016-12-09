from model_mommy import mommy


class InfantBirthMixin:
    """Adds the infant birth model."""
    def setUp(self):
        super(InfantBirthMixin, self).setUp()
        self.infant_birth = mommy.make_recipe(
            'td_infant.infantbirth',
            delivery_reference=self.maternal_lab_del.reference,
            birth_order=1,
            birth_order_denominator=1)
