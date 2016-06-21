from django.forms.models import ModelForm

from ..models import (
    InfantCongenitalAnomalies, InfantCns, InfantFacialDefect,
    InfantCleftDisorder, InfantMouthUpGi,
    InfantCardioDisorder, InfantRespiratoryDefect, InfantLowerGi,
    InfantFemaleGenital, InfantMaleGenital, InfantMusculoskeletal,
    InfantTrisomies, InfantOtherAbnormalityItems, InfantSkin,
    InfantRenal)


class InfantCongenitalAnomaliesForm(ModelForm):

    class Meta:
        model = InfantCongenitalAnomalies
        fields = '__all__'


class InfantCnsForm(ModelForm):

    class Meta:
        model = InfantCns
        fields = '__all__'


class InfantFacialDefectForm(ModelForm):

    class Meta:
        model = InfantFacialDefect
        fields = '__all__'


class InfantCleftDisorderForm(ModelForm):

    class Meta:
        model = InfantCleftDisorder
        fields = '__all__'


class InfantMouthUpGiForm(ModelForm):

    class Meta:
        model = InfantMouthUpGi
        fields = '__all__'


class InfantCardioDisorderForm(ModelForm):

    class Meta:
        model = InfantCardioDisorder
        fields = '__all__'


class InfantRespiratoryDefectForm(ModelForm):

    class Meta:
        model = InfantRespiratoryDefect
        fields = '__all__'


class InfantLowerGiForm(ModelForm):

    class Meta:
        model = InfantLowerGi
        fields = '__all__'


class InfantFemaleGenitalForm(ModelForm):

    class Meta:
        model = InfantFemaleGenital
        fields = '__all__'


class InfantMaleGenitalForm(ModelForm):

    class Meta:
        model = InfantMaleGenital
        fields = '__all__'


class InfantRenalForm(ModelForm):

    class Meta:
        model = InfantRenal
        fields = '__all__'


class InfantMusculoskeletalForm(ModelForm):

    class Meta:
        model = InfantMusculoskeletal
        fields = '__all__'


class InfantSkinForm(ModelForm):

    class Meta:
        model = InfantSkin
        fields = '__all__'


class InfantTrisomiesForm(ModelForm):

    class Meta:
        model = InfantTrisomies
        fields = '__all__'


class InfantOtherAbnormalityItemsForm(ModelForm):

    class Meta:
        model = InfantOtherAbnormalityItems
        fields = '__all__'
