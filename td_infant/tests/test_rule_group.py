from django.test import TestCase
from model_mommy import mommy

from edc_constants.constants import (POS, NEG, YES, NO)
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import RequisitionMetadata, CrfMetadata

from td.constants import NO_MODIFICATIONS, DISCONTINUED

from .test_mixins import InfantMixin


class TestRuleGroups(InfantMixin, TestCase):

    def setUp(self):
        super(TestRuleGroups, self).setUp()

    def test_congentinal_yes(self):
        """Asserts infant congenital anomalies is REQUIRED if congenital anomalies are seen."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000')
        mommy.make_recipe(
            'td_infant.infantbirthdata',
            infant_visit=self.get_infant_visit('2000'), congenital_anomalities=YES)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantcongenitalanomalies',
                visit_code='2000').count(), 1)

    def test_congentinal_no(self):
        """Asserts infant congenital anomalies is NOT_REQUIRED if congenital anomalies are seen."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000')
        mommy.make_recipe(
            'td_infant.infantbirthdata',
            infant_visit=self.get_infant_visit('2000'), congenital_anomalities=NO)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantcongenitalanomalies',
                visit_code='2000').count(), 1)

    def test_infantfu_assessment_yes(self):
        """Asserts infant fu physical is REQUIRED if physical assessment was done."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010')
        mommy.make_recipe(
            'td_infant.infantfu',
            infant_visit=self.get_infant_visit('2010'), physical_assessment=YES)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantfuphysical',
                visit_code='2010').count(), 1)

    def test_infantfu_assessment_no(self):
        """Asserts infant fu physical is NOT_REQUIRED if physical assessment was done."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010')
        mommy.make_recipe(
            'td_infant.infantfu',
            infant_visit=self.get_infant_visit('2010'), physical_assessment=NO)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantfuphysical',
                visit_code='2010').count(), 1)

    def test_infantfu_has_dx_yes(self):
        """Asserts infant diagnoses is REQUIRED if has_dx=YES."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010')
        mommy.make_recipe(
            'td_infant.infantfu',
            infant_visit=self.get_infant_visit('2010'), has_dx=YES)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantfudx',
                visit_code='2010').count(), 1)

    def test_infantfu_has_dx_no(self):
        """Asserts infant diagnoses is NOT_REQUIRED if has_dx=YES."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010')
        mommy.make_recipe(
            'td_infant.infantfu',
            infant_visit=self.get_infant_visit('2010'), has_dx=NO)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantfudx',
                visit_code='2010').count(), 1)

    def test_infant_arv_proph_required_at_2010(self):
        """Asserts infant arv proph is REQUIRED if mother is POS."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantarvproph',
                visit_code='2010').count(), 1)

    def test_infant_arv_proph_not_required_hiv_neg_mother(self):
        """Asserts infant arv proph is NOT_REQUIRED if mother is NEG."""
        self.make_infant_birth(maternal_status=NEG)
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantarvproph',
                visit_code='2010').count(), 1)

    def test_infant_arv_proph_required_at_2020(self):
        """Asserts infant arv proph is REQUIRED in future visits if mother is POS and
        arv_status=NO_MODIFICATIONS."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010')
        mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=self.get_infant_visit('2010'), prophylatic_nvp=YES, arv_status=NO_MODIFICATIONS)
        self.add_infant_visit('2020')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantarvproph',
                visit_code='2020').count(), 1)

    def test_infant_arv_proph_not_required_at_2060(self):
        """Asserts infant arv proph is NOT_REQUIRED in future visits if mother is POS and
        arv_status=DISCONTINUED."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010')
        mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=self.get_infant_visit('2010'), prophylatic_nvp=YES, arv_status=NO_MODIFICATIONS)
        self.add_infant_visit('2020')
        mommy.make_recipe(
            'td_infant.infantarvproph',
            infant_visit=self.get_infant_visit('2020'), prophylatic_nvp=YES, arv_status=DISCONTINUED)
        self.add_infant_visit('2060')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantarvproph',
                visit_code='2060').count(), 1)

    def test_infant_birth_arv(self):
        """Asserts infant birth arv is NOT_REQUIRED if mother is POS."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visit('2000')
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.infant_identifier,
                model='td_infant.infantbirtharv',
                visit_code='2000').count(), 1)

    def test_dnapcr_for_non_heu_infant(self):
        """Asserts if NON HEU infant DNA PCR requisition is NOT made available."""
        self.make_infant_birth(maternal_status=NEG)
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                subject_identifier=self.infant_identifier,
                entry_status=NOT_REQUIRED,
                model='td_lab.infantrequisition',
                panel_name='Infant HIV PCR PBMC PL',
                visit_code='2010').count(), 1)

    def test_dnapcr_for_exposed_infant(self):
        """Asserts that DNA PCR requisition is made available for an HIV exposed infant."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                subject_identifier=self.infant_identifier,
                entry_status=REQUIRED,
                model='td_lab.infantrequisition',
                panel_name='Infant HIV PCR PBMC PL',
                visit_code='2010').count(), 1)

    def test_require_infant_heel_stick_visit_2020_pos(self):
        """Assert Infant Heelstick is REQUIRED for Hiv Exposed infant."""
        self.make_infant_birth(maternal_status=POS)
        self.add_infant_visits('2000', '2010', '2020')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                subject_identifier=self.infant_identifier,
                entry_status=REQUIRED,
                model='td_lab.infantrequisition',
                panel_name='Infant Heelstick',
                visit_code='2020').count(), 1)

    def test_require_infant_heel_stick_visit_2020_neg(self):
        """Assert Infant Heelstick is NOT_REQUIRED for Hiv UnExposed infant."""
        self.make_infant_birth(maternal_status=NEG)
        self.add_infant_visits('2000', '2010', '2020')
        self.assertEqual(
            RequisitionMetadata.objects.filter(
                subject_identifier=self.infant_identifier,
                entry_status=NOT_REQUIRED,
                model='td_lab.infantrequisition',
                panel_name='Infant Heelstick',
                visit_code='2020').count(), 1)
