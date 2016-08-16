from django import forms

from edc_constants.constants import NO, YES, NOT_APPLICABLE

from tshilo_dikotla.constants import NO_MODIFICATIONS

from ..models import MaternalArvPost, MaternalArvPostMed, MaternalArvPostAdh

from .base_maternal_model_form import BaseMaternalModelForm


class MaternalArvPostForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvPostForm, self).clean()
        # if mother is not supposed to be on ARVS,then the MaternalArvPostAdh is not required
        if cleaned_data.get('on_arv_since') == NO or cleaned_data.get('arv_status') == 'never started':
            if MaternalArvPostAdh.objects.filter(maternal_visit=cleaned_data.get('maternal_visit')):
                raise forms.ValidationError("ARV history exists. You wrote mother did NOT receive ARVs "
                                            "in this pregnancy. Please correct '{}' first.".format(
                                                MaternalArvPostAdh._meta.verbose_name))
 
        if cleaned_data.get('on_arv_since') == NO and cleaned_data.get('on_arv_reason') != 'N/A':
            raise forms.ValidationError('You indicated that participant was not on HAART.'
                                        ' You CANNOT provide a reason. Please correct.')
        if cleaned_data.get('on_arv_since') == YES and cleaned_data.get('on_arv_reason') == 'N/A':
            raise forms.ValidationError("You indicated that participant was on triple ARVs. "
                                        "Reason CANNOT be 'Not Applicable'. Please correct.")

        return cleaned_data

    class Meta:
        model = MaternalArvPost
        fields = '__all__'


class MaternalArvPostMedForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvPostMedForm, self).clean()
 
        if (cleaned_data.get('maternal_arv_post').arv_status == NOT_APPLICABLE or
                cleaned_data.get('maternal_arv_post').arv_status == NO_MODIFICATIONS):
            if cleaned_data.get('arv_code'):
                raise forms.ValidationError("You cannot indicate arv modifaction as you indicated {} above."
                                            .format(cleaned_data.get('maternal_arv_post').arv_status))
        return cleaned_data

    class Meta:
        model = MaternalArvPostMed
        fields = '__all__'


class MaternalArvPostAdhForm(BaseMaternalModelForm):

    def clean(self):
        return super(MaternalArvPostAdhForm, self).clean()

    class Meta:
        model = MaternalArvPostAdh
        fields = '__all__'
