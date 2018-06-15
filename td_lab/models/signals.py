from django.db.models.signals import post_save
from django.dispatch import receiver

from .infant_requisition import InfantRequisition
from .maternal_requisition import MaternalRequisition
from .receive import Receive


@receiver(post_save, weak=False, dispatch_uid='resave_receive_record')
def resave_receive_record(sender, instance, raw, created, using, **kwargs):

    if not raw:
        if isinstance(instance, InfantRequisition) or isinstance(instance, MaternalRequisition):

            if instance.id:
                try:
                    receive = Receive.objects.get(
                        requisition_identifier=instance.requisition_identifier)
                except Receive.DoesNotExist:
                    pass
                else:
                    receive.drawn_datetime = instance.drawn_datetime
                    receive.save()
