from django.utils import timezone
from dateutil.relativedelta import relativedelta

from edc_constants.constants import (POS, YES, NO, NOT_APPLICABLE)
from edc_sync.models import OutgoingTransaction

from td_appointment.models import Appointment

from td_maternal.models import MaternalVisit

from .base_test_case import BaseTestCase
from .factories import (MaternalEligibilityFactory, MaternalConsentFactory, AntenatalEnrollmentFactory,
                        MaternalVisitFactory, MaternalLabourDelFactory, MaternalUltraSoundIniFactory,
                        AntenatalVisitMembershipFactory)


class TestOutgoingTransactions(BaseTestCase):

    def setUp(self):
        pass

    def test_outgoing_transactions_created(self):
        super(TestOutgoingTransactions, self).setUp()
        maternal_eligibility = MaternalEligibilityFactory()
        self.assertNotEqual(OutgoingTransaction.objects.all().count(), 0)
        self.assertTrue(OutgoingTransaction.objects.filter(tx_name='td_maternal.maternaleligibility').exists())
        self.options = {'registered_subject': maternal_eligibility.registered_subject,
                        'current_hiv_status': POS,
                        'evidence_hiv_status': YES,
                        'will_get_arvs': YES,
                        'is_diabetic': NO,
                        'will_remain_onstudy': YES,
                        'rapid_test_done': NOT_APPLICABLE,
                        'last_period_date': (timezone.datetime.now() - relativedelta(weeks=25)).date()}
        MaternalConsentFactory(maternal_eligibility=maternal_eligibility)
        self.registered_subject = maternal_eligibility.registered_subject
        self.assertTrue(OutgoingTransaction.objects.filter(tx_name='td_maternal.maternalconsent').exists())
        AntenatalEnrollmentFactory(**self.options)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')

        self.maternal_ultrasound = MaternalUltraSoundIniFactory(maternal_visit=self.maternal_visit_1000,
                                                                number_of_gestations=1,)

        AntenatalVisitMembershipFactory(registered_subject=self.options.get('registered_subject'))

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1010M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        MaternalLabourDelFactory(registered_subject=self.registered_subject)
        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1020M')
        MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.assertTrue(OutgoingTransaction.objects.filter(tx_name='td_maternal.antenatalenrollment').exists())
        self.assertTrue(MaternalVisit.objects.all().exists())
        self.assertTrue(OutgoingTransaction.objects.filter(tx_name='td_maternal.maternalvisit').exists())
