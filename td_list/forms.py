from django import forms
from .models import (
    ChronicConditions, Contraceptives, DiseasesAtEnrollment, HouseholdGoods,
    PriorArv, AutopsyInfoSource, Supplements, InfantVaccines, MaternalRelatives, MaternalMedications,
    Foods, Rations, Malformations, MaternalDiagnoses, DeliveryComplications, MaternalHospitalization)


class ChronicConditionsForm (forms.ModelForm):

    class Meta:
        model = ChronicConditions


class ContraceptivesForm (forms.ModelForm):

    class Meta:
        model = Contraceptives


class DeliveryComplicationsForm (forms.ModelForm):

    class Meta:
        model = DeliveryComplications


class DiseasesAtEnrollmentForm (forms.ModelForm):

    class Meta:
        model = DiseasesAtEnrollment


class HouseholdGoodsForm (forms.ModelForm):

    class Meta:
        model = HouseholdGoods


class MaternalMedicationsForm (forms.ModelForm):

    class Meta:
        model = MaternalMedications


class PriorArvForm (forms.ModelForm):

    class Meta:
        model = PriorArv


class AutopsyInfoSourceForm (forms.ModelForm):

    class Meta:
        model = AutopsyInfoSource


class FoodsForm (forms.ModelForm):

    class Meta:
        model = Foods


class RationsForm (forms.ModelForm):

    class Meta:
        model = Rations


class SupplementsForm (forms.ModelForm):

    class Meta:
        model = Supplements


class InfantVaccinesForm (forms.ModelForm):

    class Meta:
        model = InfantVaccines


class MaternalRelativesForm(forms.ModelForm):

    class Meta:
        model = MaternalRelatives


class MalformationsForm(forms.ModelForm):

    class Meta:
        model = Malformations


class MaternalDiagnosesForm(forms.ModelForm):

    class Meta:
        model = MaternalDiagnoses


class MaternalHospitalizationForm(forms.ModelForm):

    class Meta:
        model = MaternalHospitalization
