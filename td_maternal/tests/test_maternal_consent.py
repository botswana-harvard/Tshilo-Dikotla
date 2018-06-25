from .base_test_case import BaseTestCase

from .factories import MaternalEligibilityFactory, MaternalConsentFactory
from td_maternal.models import MaternalConsent
from django.utils import timezone
from td_maternal.models.td_consent_version import TdConsentVersion
from edc_consent.exceptions import ConsentVersionError


class TestMaternalConsent(BaseTestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        super(TestMaternalConsent, self).setUp()
        self.maternal_eligibility_1 = MaternalEligibilityFactory()
        self.maternal_eligibility_2 = MaternalEligibilityFactory()

    def test_pcik_old_consent_version(self):
        """Assert if latest version is picked for a newly consented participant even if version 1 is specified.
        """
        TdConsentVersion.objects.create(maternal_eligibility=self.maternal_eligibility_1, version="1", report_datetime=timezone.now())
        consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility_1)
        self.assertEqual(MaternalConsent.objects.all().count(), 1)
        self.assertEqual(consent.version, "3")

    def test_pcik_lastest_consent_version(self):
        """Assert if latest version is picked for a newly consented participant even if version 3 is specified.
        """
        TdConsentVersion.objects.create(maternal_eligibility=self.maternal_eligibility_1, version="3", report_datetime=timezone.now())
        consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility_1)
        self.assertEqual(MaternalConsent.objects.all().count(), 1)
        self.assertEqual(consent.version, "3")

    def test_pcik_no_consent_version(self):
        """Assert if no version is picked for a newly consented participant is given latest consent version.
        """
        consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility_1)
        self.assertEqual(MaternalConsent.objects.all().count(), 1)
        self.assertEqual(consent.version, "3")


    def test_re_consent_new_version(self):
        """Assert if latest version is picked for a consented participant with
        requested consent version being version 3.
        """
        consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility_1)
        consent.version="1"
        consent.save_base(raw=True)
        consent = MaternalConsent.objects.get(id=consent.id)
        self.assertEqual(consent.version, "1")
        TdConsentVersion.objects.create(maternal_eligibility=self.maternal_eligibility_1, version="3", report_datetime=timezone.now())
        consent_version2 = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility_1)
        self.assertEqual(consent_version2.version, "3")
        self.assertEqual(MaternalConsent.objects.all().count(), 2)

    def test_re_consent_new_version1(self):
        """Assert if an error is raised if trying to re consent a participant who decline a re consent.
        """
        consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility_1)
        consent.version="1"
        consent.save_base(raw=True)
        consent = MaternalConsent.objects.get(id=consent.id)
        self.assertEqual(consent.version, "1")
        TdConsentVersion.objects.create(maternal_eligibility=self.maternal_eligibility_1, version="1", report_datetime=timezone.now())
        expected_message = 'Re Consenting declided by participant as per the TdConsentVersion form'
        with self.assertRaisesMessage(ConsentVersionError, expected_message):
            MaternalConsentFactory(
                maternal_eligibility=self.maternal_eligibility_1)

    def test_re_consent_new_version2(self):
        """Assert if an error is raised if trying to re consent a participant who is not offered a consent version form,
        to accept or decline a re consent
        """
        consent = MaternalConsentFactory(
            maternal_eligibility=self.maternal_eligibility_1)
        consent.version="1"
        consent.save_base(raw=True)
        consent = MaternalConsent.objects.get(id=consent.id)
        self.assertEqual(consent.version, "1")
        expected_message = 'Please fill in the TD consent version form first.'
        with self.assertRaisesMessage(ConsentVersionError, expected_message):
            MaternalConsentFactory(
                maternal_eligibility=self.maternal_eligibility_1)
