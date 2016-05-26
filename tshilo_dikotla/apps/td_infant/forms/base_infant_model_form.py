from edc_base.form.forms import BaseModelForm

from ..models import InfantVisit


class BaseInfantModelForm(BaseModelForm):

    visit_model = InfantVisit
