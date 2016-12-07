from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_constants.constants import ALIVE, ON_STUDY, FAILED_ELIGIBILITY
from edc_visit_tracking.constants import SCHEDULED

from td.models import Appointment

from .antenatal_enrollment import AntenatalEnrollment
from .maternal_eligibility import MaternalEligibility
from .maternal_offstudy import MaternalOffstudy
from .maternal_visit import MaternalVisit
from td_maternal.models.maternal_ultrasound_initial import MaternalUltraSoundInitial


@receiver(post_save, weak=False, sender=MaternalEligibility, dispatch_uid="maternal_eligibility_on_post_save")
def maternal_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw and not kwargs.get('update_fields'):
        instance.create_update_or_delete_eligibility_loss()


@receiver(post_save, sender=AntenatalEnrollment, weak=False, dispatch_uid="ineligible_take_off_study")
def create_offstudy_on_ineligible(sender, instance, raw, created, using, **kwargs):
    """If not eligible, create off study."""
    if not raw:
        try:
            if not instance.is_eligible and not instance.pending_ultrasound:
                MaternalOffstudy.objects.create(
                    subject_identifier=instance.subject_identifier,
                    offstudy_datetime=instance.report_datetime,
                    reason=FAILED_ELIGIBILITY,
                    comment=instance.reasons_not_eligible)
        except AttributeError as e:
            if 'is_eligible' not in str(e) and 'pending_ultrasound' not in str(e):
                raise AttributeError(str(e))


@receiver(post_save, sender=AntenatalEnrollment, weak=False, dispatch_uid="eligible_put_back_on_study")
def delete_offstudy_on_eligible(sender, instance, raw, created, using, **kwargs):
    """If eligible, delete off study."""
    if not raw:
        try:
            if instance.pending_ultrasound or instance.is_eligible:
                MaternalOffstudy.objects.filter(subject_identifier=instance.subject_identifier).delete()
        except AttributeError as e:
            if 'is_eligible' not in str(e) and 'registered_subject' not in str(e):
                raise


@receiver(post_save, weak=False, sender=MaternalUltraSoundInitial, dispatch_uid="maternal_ultrasound_on_post_save")
def maternal_ultrasound_delivery_initial_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Update antenatal enrollment to re-assess eligibility based on ultrasound."""
    if not raw:
        # if isinstance(instance, MaternalUltraSoundInitial):  # or isinstance(instance, MaternalLabourDel):
        antenatal_enrollment = AntenatalEnrollment.objects.get(
            subject_identifier=instance.maternal_visit.subject_identifier)
        antenatal_enrollment.pending_ultrasound = False
        antenatal_enrollment.save()
