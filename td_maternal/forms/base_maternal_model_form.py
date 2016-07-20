from edc_base.form.old_forms import BaseModelForm

from ..models import MaternalVisit
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS, NEG


class BaseMaternalModelForm(BaseModelForm):

    visit_model = MaternalVisit

    def validate_many_to_many_not_blank(self, field):
        """check if the many to many field is blank"""

        cleaned_data = self.cleaned_data

        if not cleaned_data.get(field):
            return True

    def validate_not_applicable_and_other_options(self, field):
        """check if not applicable has been selected along with other options"""

        cleaned_data = self.cleaned_data
        many2many_qs = cleaned_data.get(field).values_list('short_name', flat=True)
        many2many_list = list(many2many_qs.all())

        if NOT_APPLICABLE in many2many_list and len(many2many_list) > 1:
            return True

    def validate_not_applicable_not_there(self, field):
        """check if not applicable is not there when it is supposed to be"""

        cleaned_data = self.cleaned_data
        many2many_qs = cleaned_data.get(field).values_list('short_name', flat=True)
        many2many_list = list(many2many_qs.all())

        if NOT_APPLICABLE not in many2many_list:
            return True

    def validate_not_applicable_in_there(self, field):
        """check if not applicable is there"""

        cleaned_data = self.cleaned_data
        many2many_qs = cleaned_data.get(field).values_list('short_name', flat=True)
        many2many_list = list(many2many_qs.all())

        if NOT_APPLICABLE in many2many_list:
            return True