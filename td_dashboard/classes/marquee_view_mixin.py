from collections import OrderedDict
from django.apps import apps
from django.urls.base import reverse


class MarqueeViewMixin:

    def __init__(self):
        self.context = {}
        self.markey_next_row = 4
        self.consent_model = None
        self.membership_form_category = []

    def get_context_data(self, **kwargs):
        self.context = super(MarqueeViewMixin, self).get_context_data(**kwargs)
        return self.context

    @property
    def marquee_data(self):
        marquee_data = OrderedDict()
        if self.consent:
            marquee_data['Name'] = '{}({})'.format(self.consent.first_name, self.consent.initials),
            marquee_data['Born'] = self.consent.dob,
            marquee_data['Age'] = self.age,
            marquee_data['Consented'] = self.consent.consent_datetime,
            marquee_data['Antenatal enrollment status'] = self.maternal_marquee_data.get('antenatal_enrollment_status'),
            marquee_data['Enrollment HIV status'] = self.maternal_marquee_data.get('enrollment_hiv_status'),
            marquee_data['Current HIV status'] = self.maternal_marquee_data.get('current_hiv_status'),
            marquee_data['Pregnant, GA'] = self.maternal_marquee_data.get('gestational_age'),
            marquee_data['Planned delivery site'] = self.maternal_marquee_data.get('delivery_site'),
            marquee_data['Randomized'] = self.maternal_marquee_data.get('randomized')
        return marquee_data

    @property
    def maternal_marquee_data(self):
        return {}

    @property
    def consent(self):
        return self.consent_model

    @property
    def age(self):
        return None

    @property
    def age_today(self):
        return None

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
