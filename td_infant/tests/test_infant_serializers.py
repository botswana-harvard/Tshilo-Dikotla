import json

from django.core import serializers
from django.test.testcases import TestCase

from edc_constants.constants import POS
from edc_sync.test_mixins import SyncTestSerializerMixin
from edc_sync.models import OutgoingTransaction
from edc_visit_tracking.constants import SCHEDULED


from model_mommy import mommy

from td.models import Appointment

from .test_mixins import InfantMixin
from .test_mixins import InfantTestMixin, CompleteInfantCrfsMixin

class TestInfantSerializers(SyncTestSerializerMixin, InfantMixin, TestCase):

    def setUp(self):
        super(TestInfantSerializers, self).setUp()
                
    def test_visit_2000(self):
        self.make_infant_birth(maternal_status=POS)
        for visit in self.infant_birth.schedule.visits:
            complete_required_maternal_crfs = self.complete_required_infant_crfs(visit.code)
            self.sync_test_serializers_for_visit(complete_required_maternal_crfs, verbose=False)

