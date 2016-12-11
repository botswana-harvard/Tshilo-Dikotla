from django.test import TestCase, tag

from edc_sync.test_mixins import SyncTestSerializerMixin

from .test_mixins import MotherMixin
from edc_visit_schedule.site_visit_schedules import site_visit_schedules


@tag('review', 'slow')
class TestNaturalKey(SyncTestSerializerMixin, MotherMixin, TestCase):

    def test_natural_key_attrs(self):
        self.sync_test_natural_key_attr('td', 'td_infant', 'td_maternal', 'td_lab')

    def test_get_by_natural_key_attr(self):
        self.sync_test_get_by_natural_key_attr('td', 'td_infant', 'td_maternal', 'td_lab')

    @tag('crf_natural_keys')
    def test_crf_natural_keys(self):
        verbose = True
        self.make_positive_mother()
        complete_required_crfs = self.complete_required_crfs('1000M')
        self.sync_test_natural_keys(complete_required_crfs, verbose=verbose)
        self.make_antenatal_enrollment_two()
        complete_required_crfs = self.complete_required_crfs('1010M')
        self.sync_test_natural_keys(complete_required_crfs, verbose=verbose)
        complete_required_crfs = self.complete_required_crfs('1020M')
        self.sync_test_natural_keys(complete_required_crfs, verbose=verbose)
        maternal_delivery = self.make_delivery()
        self.sync_test_natural_keys_by_schedule(maternal_delivery, verbose=verbose)
