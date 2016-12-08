from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from django import forms
from django.urls.base import reverse


class SearchForm(forms.Form):

    search_term = forms.CharField(
        label='Search',
        max_length=36,
        required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('search_url')
        self.helper.form_id = 'search_form'
        self.helper.form_method = 'post'
        self.helper.html5_required = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            FieldWithButtons('search_term', StrictButton('Search', type='submit')))
