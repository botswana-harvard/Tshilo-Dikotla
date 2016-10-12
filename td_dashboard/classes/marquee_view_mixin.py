

class MarqueeViewMixin:

    def __init__(self):
        self.context = {}
        self.markey_next_row = 15
        self.consent_model = None

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
