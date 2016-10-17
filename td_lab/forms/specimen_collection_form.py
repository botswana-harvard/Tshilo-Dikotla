from django import forms

from ..models import SpecimenCollection, SpecimenCollectionItem


class SpecimenCollectionForm(forms.ModelForm):

    class Meta:
        model = SpecimenCollection
        fields = '__all__'


class SubjectConsentItemForm(forms.ModelForm):

    class Meta:
        model = SpecimenCollectionItem
        fields = '__all__'
