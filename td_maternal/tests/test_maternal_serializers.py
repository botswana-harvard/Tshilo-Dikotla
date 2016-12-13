from django.test import TestCase, tag

from edc_sync.test_mixins import SyncTestSerializerMixin

from .test_mixins import MotherMixin


@tag('review')
class TestMaternalSerializers(SyncTestSerializerMixin, MotherMixin, TestCase):

    def test_1000M_NEG(self):
        self.make_negative_mother()
        complete_required_maternal_crfs = self.complete_required_maternal_crfs('1000M')
        self.sync_test_serializers_for_visit(complete_required_maternal_crfs, verbose=False)

    def test_1000M_POS(self):
        self.make_positive_mother()
        complete_required_maternal_crfs = self.complete_required_maternal_crfs('1000M')
        self.sync_test_serializers_for_visit(complete_required_maternal_crfs, verbose=False)
