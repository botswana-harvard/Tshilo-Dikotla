from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_constants.constants import (UNKNOWN,
    YES, NEG, NOT_APPLICABLE, POS, NO, SCHEDULED, CONTINUOUS, STOPPED, RESTARTED)
from edc_code_lists.models import WcsDxAdult
from edc_appointment.models import Appointment

from td_list.models import MaternalDiagnoses
from td_maternal.models import MaternalVisit, RegisteredSubject
from td_maternal.forms import MaternalPostPartumFuForm

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalVisitMembershipFactory, MaternalRandomizationFactory,
                        MaternalVisitFactory, MaternalArvPregFactory, MaternalLabourDelFactory)


class TestMaternalPostPartumFu(BaseTestCase):

    def setUp(self):
        super(TestMaternalPostPartumFu, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        self.assertEqual(RegisteredSubject.objects.all().count(), 1)

#         self.create_mother()
        self.diagnoses = MaternalDiagnoses.objects.create(
            hostname_created="django", name="Gestational Hypertension",
            short_name="Gestational Hypertension", created=timezone.datetime.now(),
            user_modified="", modified=timezone.datetime.now(),
            hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None, revision=None)

        self.diagnoses_na = MaternalDiagnoses.objects.create(
            hostname_created="django", name="N/A",
            short_name="N/A", created=timezone.datetime.now(),
            user_modified="", modified=timezone.datetime.now(),
            hostname_modified="django", version="1.0",
            display_index=1, user_created="django", field_name=None,
            revision=":develop:")

        self.who_dx = WcsDxAdult.objects.create(
            hostname_created="cabel", code="CS4003", short_name="Recurrent severe bacterial pneumo",
            created=timezone.datetime.now(), user_modified="", modified=timezone.datetime.now(),
            hostname_modified="cabel",
            long_name="Recurrent severe bacterial pneumonia", user_created="abelc",
            list_ref="WHO CLINICAL STAGING OF HIV INFECTION 2006", revision=None)

        self.who_dx_na = WcsDxAdult.objects.create(
            hostname_created="cabel", code="cs9999999", short_name="N/A",
            created=timezone.datetime.now(), user_modified="", modified=timezone.datetime.now(),
            hostname_modified="cabel", long_name="N/A",
            user_created="abelc", list_ref="", revision=None)

        self.options = {
            'new_diagnoses': YES,
            'diagnoses': [self.diagnoses.id],
            'hospitalized': YES,
            'hospitalization_reason': 'Unexplained fever',
            'hospitalization_days': 1,
            'has_who_dx': YES,
            'who': [self.who_dx.id]}

    def test_diagnosis_list_none(self):
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.options['diagnoses'] = None
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Diagnosis field should not be left empty', errors)

    def test_new_diagnoses_no_diagnosis_list_no_not_applicable(self):
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.options['new_diagnoses'] = NO
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Participant has no new diagnoses, do not give a listing, rather give N/A', errors)

    def test_new_diagnoses_no_diagnosis_list_listed_has_not_applicable(self):
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.options['new_diagnoses'] = NO
        self.options['diagnoses'] = [self.diagnoses.id, self.diagnoses_na.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Participant has no new diagnoses, do not give a listing, only give N/A', errors)

    def test_new_diagnoses_yes_diagnosis_list_has_not_applicable(self):
        self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
        delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.options['diagnoses'] = [self.diagnoses_na.id]
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question4: Participant has new diagnoses, list of diagnosis cannot be N/A', errors)

    def test_hospitalized_yes_hospitalization_reason_none(self):
        self.options['hospitalization_reason'] = None
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question7: Patient was hospitalized, please give hospitalization_reason.', errors)

    def test_hospitalized_yes_hospitalization_reason_not_other(self):
        self.options['hospitalization_other'] = 'Asthma'
        form = MaternalPostPartumFuForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Question7: Patient was hospitalized, please give hospitalization_reason.', errors)

# #     def test_hospitalized_no(self):
# #         self.options['hospitalized'] = NO
# #         form = MaternalPostPartumFuForm(data=self.options)
# #         errors = ''.join(form.errors.get('__all__'))
# #         self.assertIn('Patient was not hospitalized, please do not give hospitalization_reason.', errors)
# # 
# #     def test_mother_negative_who_diagnosis_yes(self):
# #         self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
# #         delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
# #         self.options['maternal_visit'] = self.maternal_visit_1000.id
# #         form = MaternalPostPartumFuForm(data=self.options)
# #         errors = ''.join(form.errors.get('__all__'))
# #         self.assertIn('The mother is Negative, question 10 for WHO Stage III/IV should be N/A', errors)
# # 
# #     def test_mother_negative_who_listing_yes(self):
# #         self.create_mother(self.hiv_neg_mother_options(self.registered_subject))
# #         delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
# #         self.options['maternal_visit'] = self.maternal_visit_1000.id
# #         self.options['has_who_dx'] = NOT_APPLICABLE
# #         form = MaternalPostPartumFuForm(data=self.options)
# #         errors = ''.join(form.errors.get('__all__'))
# #         self.assertIn('The mother is Negative, question 11 for WHO Stage III/IV listing should be N/A', errors)
# # 
# #     def test_mother_positive_who_diagnosis_not_applicable(self):
# #         self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
# #         delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
# #         self.options['maternal_visit'] = self.maternal_visit_1000.id
# #         self.options['has_who_dx'] = NOT_APPLICABLE
# #         form = MaternalPostPartumFuForm(data=self.options)
# #         errors = ''.join(form.errors.get('__all__'))
# #         self.assertIn('The mother is positive, question 10 for WHO Stage III/IV should not be N/A', errors)
# # 
# #     def test_mother_positive_who_diagnosis_yes_who_listing_not_applicable(self):
# #         self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
# #         delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
# #         self.options['maternal_visit'] = self.maternal_visit_1000.id
# #         self.options['who'] = [self.who_dx_na.id]
# #         form = MaternalPostPartumFuForm(data=self.options)
# #         errors = ''.join(form.errors.get('__all__'))
# #         self.assertIn('WHO diagnosis is Yes, please give who diagnosis listing.', errors)
# # 
# #     def test_mother_positive_who_diagnosis_no_who_listing_given(self):
# #         self.create_mother(self.hiv_pos_mother_options(self.registered_subject))
# #         delivery = MaternalLabourDelFactory(registered_subject=self.registered_subject)
# #         self.options['maternal_visit'] = self.maternal_visit_1000.id
# #         self.options['has_who_dx'] = NO
# #         form = MaternalPostPartumFuForm(data=self.options)
# #         errors = ''.join(form.errors.get('__all__'))
# #         self.assertIn(
# #             'The mother has no new WHO Stage III/IV diagnosis, please do not give a listing, rather select N/A', errors)
