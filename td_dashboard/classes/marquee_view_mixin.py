from django.apps import apps
from django.urls.base import reverse


class MarqueeViewMixin:

    def __init__(self):
        self.context = {}
        self.markey_next_row = 15
        self.consent_model = None
        self.membership_form_category = []

    def get_context_data(self, **kwargs):
        self.context = super(MarqueeViewMixin, self).get_context_data(**kwargs)
        return self.context

    @property
    def markey_data(self):
        markey_data = {}
        if self.consent:
            markey_data = {
                'Name': '{}({})'.format(self.consent.first_name, self.consent.initials),
                'Born': self.consent.dob,
                'Age': self.age,
                'Consented': self.consent.consent_datetime,
                'Omang': self.consent.identity,
                'Gender': self.gender,
                'Age Today': self.age_today,
                'Identifier': self.consent.subject_identifier,
            }
        return markey_data

    @property
    def consent(self):
        return self.consent_model

    @property
    def age(self):
        return None

    @property
    def age_today(self):
        return None

    @property
    def gender(self):
        gender = 'Female' if self.consent.gender == 'F' else 'Male'
        return gender

    def subject_membership_models(self):
        """ """
        self._subject_membership_models = []
        for model_lower in self.membership_form_category:
            app_label, model_name = model_lower.split('.')
            model = apps.get_app_config('td_maternal').get_model(model_name)
            obj = None
            try:
                obj = model.objects.get(registered_subject__subject_identifier=self.subject_identifier)
                admin_model_url_label = "{}({})".format(model._meta.verbose_name, 'complete')
                admin_model_change_url = obj.get_absolute_url()
                self._subject_membership_models.append([admin_model_url_label, admin_model_change_url])
            except model.DoesNotExist:
                admin_model_url_label = "{}({})".format(model._meta.verbose_name, 'new')
                admin_model_add_url = reverse('admin:{}_{}_add'.format(app_label, model_name))
                self._subject_membership_models.append([admin_model_url_label, admin_model_add_url])
        return self._subject_membership_models
