from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from edc_constants.constants import (YES, NOT_APPLICABLE, POS, NO, CONTINUOUS, STOPPED, RESTARTED)
from edc_visit_tracking.constants import SCHEDULED

from td_appointment.models import Appointment
from td_list.models import PriorArv
from td_maternal.models import MaternalVisit, RegisteredSubject
from td_maternal.forms import MaternalLifetimeArvHistoryForm

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, MaternalObstericHistoryFactory, MaternalVisitFactory)


class TestMaternalLifetimeArvHistoryForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalLifetimeArvHistoryForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility)
        self.registered_subject = self.maternal_eligibility.registered_subject

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

        self.appointment = Appointment.objects.get(
            subject_identifier=self.registered_subject.subject_identifier, visit_code='1000M')
        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment, reason='scheduled')
        self.maternal_ultrasound = MaternalUltraSoundIniFactory(
            maternal_visit=self.maternal_visit_1000, number_of_gestations=1)

        prior_arv = PriorArv.objects.create(
            hostname_created="django", name="Atripla", short_name="Atripla",
            created="2016-23-20T15:05:12.799", user_modified="", modified="2016-23-20T15:05:12.799", 
            hostname_modified="django", version="1.0", display_index=1, user_created="django", 
            field_name=None, revision=":develop")

        self.options = {
            'maternal_visit': self.maternal_visit_1000.id,
            'report_datetime': timezone.now(),
            'haart_start_date': datetime.today() - relativedelta(months=9),
            'is_date_estimated': '-',
            'preg_on_haart': YES,
            'haart_changes': 0,
            'prior_preg': CONTINUOUS,
            'prior_arv': [prior_arv.id]}

    def test_arv_interrupt_1(self):
        """Assert that if was not still on ARV then 'interruption never restarted'
        is not a valid option."""

        self.options['prior_preg'] = STOPPED
        self.options['haart_start_date'] = date(2015, 4, 10)
        self.options['preg_on_haart'] = YES
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("You indicated that the mother was still on triple ARV when "
                      "she got pregnant, yet you indicated that ARVs were interrupted "
                      "and never restarted.", errors)

    def test_arv_interrupt_2(self):
        """Assert that if was not on ARV then 'Had treatment
        interruption but restarted' is not a valid option."""
        self.options['preg_on_haart'] = NO
        self.options['prior_preg'] = RESTARTED
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that the mother was NOT on triple ARV when she got pregnant. '
            'ARVs could not have been interrupted. Please correct.', errors)

    def test_arv_interrupt_3(self):
        """Assert that if was not still on ARV then 'Received continuous HAART from the
        time she started is not a valid option."""
        self.options['preg_on_haart'] = NO
        self.options['prior_preg'] = CONTINUOUS
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that the mother was NOT on triple ARV when she got pregnant. '
            'ARVs could not have been uninterrupted. Please correct.', errors)

    def test_arv_interrupt_4(self):
        """Assert that if was not still on ARV only valid answer is 'interrupted and never
        restarted'"""
        self.options['preg_on_haart'] = YES
        self.options['prior_preg'] = STOPPED
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        self.assertIn(
            'You indicated that the mother was still on triple ARV when she got pregnant, '
            'yet you indicated that ARVs were interrupted and never restarted. Please correct.', 
            form.errors.get('__all__'))

    def test_haart_start_date_2(self):
        """Start date of ARVs CANNOT be before DOB"""
        MaternalObstericHistoryFactory(maternal_visit=self.maternal_visit_1000, prev_pregnancies=1)
        self.options['prev_sdnvp_labour'] = NOT_APPLICABLE
        self.options['prev_preg_azt'] = NOT_APPLICABLE
        self.options['prev_preg_haart'] = YES
        self.options['haart_start_date'] = date(1987, 10, 10)
        self.options['report_datetime'] = datetime.today()
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("Date of triple ARVs first started CANNOT be before DOB.", errors)

    def test_haart_start_date_none(self):
        """Start date of ARVs CANNOT be None"""
        MaternalObstericHistoryFactory(maternal_visit=self.maternal_visit_1000, prev_pregnancies=1)
        self.options['prev_sdnvp_labour'] = NOT_APPLICABLE
        self.options['prev_preg_azt'] = NOT_APPLICABLE
        self.options['prev_preg_haart'] = YES
        self.options['haart_start_date'] = None
        self.options['report_datetime'] = datetime.today()
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("Please give a valid arv initiation date.", errors)

    def test_prev_preg_azt(self):
        MaternalObstericHistoryFactory(maternal_visit=self.maternal_visit_1000, prev_pregnancies=0)
        self.options['prev_preg_azt'] = YES
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'In Maternal Obsterical History form you indicated there were no previous '
            'pregnancies. Receive AZT monotherapy in previous pregancy should be '
            'NOT APPLICABLE', errors)

    def test_prev_sdnvp_labour(self):
        MaternalObstericHistoryFactory(maternal_visit=self.maternal_visit_1000, prev_pregnancies=0)
        self.options['prev_sdnvp_labour'] = YES
        self.options['prev_preg_azt'] = NOT_APPLICABLE
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'In Maternal Obsterical History form you indicated there were no previous '
            'pregnancies. Single sd-NVP in labour during a prev pregnancy should '
            'be NOT APPLICABLE', errors)

    def test_prev_preg_haart(self):
        MaternalObstericHistoryFactory(maternal_visit=self.maternal_visit_1000, prev_pregnancies=0)
        self.options['prev_sdnvp_labour'] = NOT_APPLICABLE
        self.options['prev_preg_azt'] = NOT_APPLICABLE
        self.options['prev_preg_haart'] = YES
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'In Maternal Obsterical History form you indicated there were no previous '
            'pregnancies. triple ARVs during a prev pregnancy should '
            'be NOT APPLICABLE', errors)
