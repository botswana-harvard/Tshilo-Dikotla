from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from edc_constants.constants import (UNKNOWN, 
    YES, NEG, NOT_APPLICABLE, POS, NO, SCHEDULED, CONTINUOUS, STOPPED, RESTARTED)
from tshilo_dikotla.apps.td_list.models import MaternalDiagnoses
from tshilo_dikotla.apps.td_maternal.models import MaternalVisit, RegisteredSubject
from tshilo_dikotla.apps.td_maternal.forms import MaternalArvPregForm, MaternalArvForm

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalVisitMembershipFactory, MaternalRandomizationFactory,
                        MaternalVisitFactory, MaternalArvPregFactory)


class TestMaternalArvPregForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalArvPregForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        options = {'registered_subject': self.registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        self.antenatal_enrollment = AntenatalEnrollmentFactory(**options)
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit, number_of_gestations=1,)

        diagnoses = MaternalDiagnoses.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        
        self.who_dx = WcsDxAdult.objects.create(
            hostname_created="cabel", code="CS4003", short_name="Recurrent severe bacterial pneumo",
            created=timezone.datetime.now(), user_modified="", modified=timezone.datetime.now(), hostname_modified="cabel", long_name="Recurrent severe bacterial pneumonia", 
            user_created="abelc", list_ref="WHO CLINICAL STAGING OF HIV INFECTION 2006", revision=None)
    
        self.options = {
                'new_diagnoses': YES,
                'diagnoses': diagnoses.id,
                'has_who_dx': YES,
                'who': self.who_dx.id
                }

    def test_has_diagnoses(self):
        