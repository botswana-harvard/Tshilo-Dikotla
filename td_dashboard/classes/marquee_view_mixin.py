from collections import OrderedDict


class MarqueeViewMixin:

    def __init__(self):
        self.context = {}
        self.markey_next_row = 4
        self.consent_model = None
        self.enrollments_models = []
        self.dashboard = None

    def get_context_data(self, **kwargs):
        self.context = super(MarqueeViewMixin, self).get_context_data(**kwargs)
        return self.context

    @property
    def demographics(self):
        demographics = OrderedDict()
        if self.consent:
            demographics['Name'] = '{}({})'.format(self.consent.first_name, self.consent.initials),
            demographics['Born'] = self.consent.dob,
            demographics['Age'] = self.age,
            demographics['Consented'] = self.consent.consent_datetime,
            demographics['Antenatal enrollment status'] = self.demographics_data.get('antenatal_enrollment_status'),
            demographics['Enrollment HIV status'] = self.demographics_data.get('enrollment_hiv_status'),
            demographics['Current HIV status'] = self.demographics_data.get('current_hiv_status'),
            demographics['Pregnant, GA'] = self.demographics_data.get('gestational_age'),
            demographics['Planned delivery site'] = self.demographics_data.get('delivery_site'),
            demographics['Randomized'] = self.demographics_data.get('randomized')
        return demographics

    @property
    def demographics_data(self):
        return {}

    @property
    def consent(self):
        return self.consent_model

    @property
    def age(self):
        return None
