from edc_base.form.forms import BaseModelForm

from ..models import MaternalVisit


class BaseMaternalModelForm(BaseModelForm):

    visit_model = MaternalVisit
