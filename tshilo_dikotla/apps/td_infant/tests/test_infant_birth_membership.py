from dateutil.relativedelta import relativedelta
from edc_constants.constants import SCREENED
from edc_registration.models import RegisteredSubject
from edc_identifier.models import SubjectIdentifier
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED
from edc_meta_data.models import RequisitionMetaData
from edc_appointment.models import Appointment

from tshilo_dikotla.apps.td_maternal.models import MaternalVisit

from tshilo_dikotla.apps.td_maternal.tests import BaseTestCase
from tshilo_dikotla.apps.td_maternal.tests.factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory,
                                                             MaternalConsentFactory, AntenatalEnrollmentFactory,
                                                             AntenatalVisitMembershipFactory, MaternalLabourDelFactory)

from .factories import InfantBirthFactory


class TestInfantBirthMembership(BaseTestCase):

    def setUp(self):
        super(TestInfantBirthMembership, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        # maternal visit created here.
        self.antenatal_enrollment = AntenatalEnrollmentFactory(registered_subject=self.registered_subject)
        self.maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=self.registered_subject,
            reason=SCHEDULED,
            appointment__visit_definition__code='1000M')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit,
                                                                number_of_gestations=1)
        self.maternal_visits_membership = AntenatalVisitMembershipFactory(registered_subject=self.registered_subject)
        self.maternal_labour_del = MaternalLabourDelFactory(registered_subject=self.registered_subject,
                                                            live_infants_to_register=1)

    def test_create_appointments(self):
        infant_birth = InfantBirthFactory(
            maternal_labour_del=self.maternal_labour_del,
            registered_subject=RegisteredSubject.objects.get(
                relative_identifier=self.maternal_consent.subject_identifier))
        self.assertEqual(Appointment.objects.filter(
            registered_subject=RegisteredSubject.objects.get(
                relative_identifier=self.maternal_consent.subject_identifier)).count(), 6)
    