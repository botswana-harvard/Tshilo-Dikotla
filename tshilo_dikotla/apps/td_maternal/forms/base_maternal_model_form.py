from edc_base.form.old_forms import BaseModelForm

from ..models import MaternalVisit


class BaseMaternalModelForm(BaseModelForm):

    visit_model = MaternalVisit
