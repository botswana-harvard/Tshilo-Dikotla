from edc_base.form.old_forms import BaseModelForm

from ..models import TdConsentVersion


class TdConsentVersionForm(BaseModelForm):

    def clean(self):
        return super(TdConsentVersionForm, self).clean()

    class Meta:
        model = TdConsentVersion
        fields = '__all__'
