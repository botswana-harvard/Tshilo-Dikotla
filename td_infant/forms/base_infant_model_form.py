from edc_base.form.old_forms import BaseModelForm

from ..models import InfantVisit


class BaseInfantModelForm(BaseModelForm):

    visit_model = InfantVisit
