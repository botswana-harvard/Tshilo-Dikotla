from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.utils import timezone

from edc_constants.constants import (UNKNOWN, 
    YES, NEG, NOT_APPLICABLE, POS, NO, SCHEDULED, CONTINUOUS, STOPPED, RESTARTED)
from td_list.models import PriorArv
from td_maternal.models import MaternalVisit, RegisteredSubject
from td_maternal.forms import MaternalLifetimeArvHistoryForm

from .base_test_case import BaseTestCase
from .factories import (MaternalUltraSoundIniFactory, MaternalEligibilityFactory, MaternalConsentFactory,
                        AntenatalEnrollmentFactory, AntenatalVisitMembershipFactory, MaternalRandomizationFactory,
                        MaternalVisitFactory)


class TestMaternalLifetimeArvHistoryForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalLifetimeArvHistoryForm, self).setUp()
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

        prior_arv = PriorArv.objects.create(
            hostname_created= "django", name="Atripla", short_name="Atripla", 
            created="2016-23-20T15:05:12.799", user_modified="", modified="2016-23-20T15:05:12.799", 
            hostname_modified="django", version="1.0", display_index=1, user_created="django", 
            field_name=None, revision=":develop")

        self.options = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'haart_start_date': datetime.today() - relativedelta(weeks=7),
            'is_date_estimated': '-',
            'preg_on_haart': YES,
            'haart_changes': 0,
            'prior_preg': CONTINUOUS,
            'prior_arv': [prior_arv.id],}

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

    def test_haart_start_date(self):
        """ARV start date should be six weeks prior to today"""
        self.options['haart_start_date'] = timezone.now()
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("ARV start date must be six weeks prior to today's date or greater.", errors)

    def test_haart_start_date_2(self):
        """Start date of ARVs CANNOT be before DOB"""
        self.options['haart_start_date'] = date(1987, 10, 10)
        self.options['report_datetime'] = datetime.today()
        form = MaternalLifetimeArvHistoryForm(data=self.options)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("Date of triple ARVs first started CANNOT be before DOB.", errors)
