from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.urls.base import reverse


class MaternalEligibilityCrispyForm(forms.Form):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        max_length=36)

    def __init__(self, *args, **kwargs):
        super(MaternalEligibilityCrispyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper = FormHelper()
        self.helper.form_action = reverse('search_url')
        self.helper.form_id = 'maternaleligibility-crispy-form-search'
        self.helper.form_method = 'post'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            FieldWithButtons('subject_identifier', StrictButton('Search', type='submit')))
