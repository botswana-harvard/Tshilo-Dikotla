from django.test import TestCase, tag

from edc_constants.constants import POS
from edc_sync.test_mixins import SyncTestSerializerMixin

from .test_mixins import InfantMixin
from edc_visit_schedule.site_visit_schedules import site_visit_schedules


@tag('review', 'slow')
class TestInfantNaturalKey(SyncTestSerializerMixin, InfantMixin, TestCase):

    @tag('crf_natural_keys')
    def test_crf_natural_keys(self):
        self.make_infant_birth(maternal_status=POS)
        infant_visits = self.add_infant_visits(*[visit.code for visit in self.infant_birth.schedule.visits])
        self.sync_test_natural_keys_by_schedule(
            visits=infant_visits,
            verbose=True,
            visit_attr='infant_visit')
