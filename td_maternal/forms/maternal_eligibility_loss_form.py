from django.forms import ModelForm

from ..models import MaternalEligibilityLoss


class MaternalEligibilityLossForm(ModelForm):

    class Meta:
        model = MaternalEligibilityLoss
        fields = '__all__'
