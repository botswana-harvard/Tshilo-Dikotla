from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from edc_constants.constants import FAILED_ELIGIBILITY

from .antenatal_enrollment import AntenatalEnrollment
from .maternal_consent import MaternalConsent
from .maternal_eligibility import MaternalEligibility
from .maternal_lab_del import MaternalLabDel
from .maternal_offstudy import MaternalOffstudy
from .maternal_ultrasound_initial import MaternalUltraSoundInitial


@receiver(post_save, weak=False, sender=MaternalEligibility, dispatch_uid="maternal_eligibility_on_post_save")
def maternal_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        instance.create_update_or_delete_eligibility_loss()


@receiver(post_delete, weak=False, sender=AntenatalEnrollment,
          dispatch_uid="delete_offstudy_on_antenatalenrollment_post_delete")
def delete_offstudy_on_antenatalenrollment_post_delete(sender, instance, **kwargs):
    MaternalOffstudy.objects.filter(subject_identifier=instance.subject_identifier).delete()


@receiver(post_save, weak=False, sender=MaternalConsent, dispatch_uid="maternal_consent_on_post_save")
def maternal_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        maternal_eligibility = MaternalEligibility.objects.get(reference=instance.maternal_eligibility_reference)
        maternal_eligibility.subject_identifier = instance.subject_identifier
        maternal_eligibility.save()


# @receiver(post_save, sender=AntenatalEnrollment, weak=False, dispatch_uid="ineligible_take_off_study")
# def create_offstudy_on_ineligible(sender, instance, raw, created, using, **kwargs):
#     """If not eligible, create off study."""
#     if not raw:
#         try:
#             if not instance.is_eligible:
#                 MaternalOffstudy.objects.create(
#                     subject_identifier=instance.subject_identifier,
#                     offstudy_datetime=instance.report_datetime,
#                     reason=FAILED_ELIGIBILITY,
#                     comment=instance.reasons_not_eligible)
#         except AttributeError as e:
#             if 'is_eligible' not in str(e):
#                 raise AttributeError(str(e))


@receiver(post_save, sender=AntenatalEnrollment, weak=False, dispatch_uid="eligible_put_back_on_study")
def delete_offstudy_on_eligible(sender, instance, raw, created, using, **kwargs):
    """If eligible, delete off study."""
    if not raw:
        try:
            if instance.is_eligible:
                MaternalOffstudy.objects.filter(subject_identifier=instance.subject_identifier).delete()
        except AttributeError as e:
            if 'is_eligible' not in str(e):
                raise AttributeError(str(e))


@receiver(post_save, weak=False, sender=MaternalUltraSoundInitial,
          dispatch_uid="maternal_ultrasound_initial_on_post_save")
def maternal_ultrasound_initial_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Update antenatal enrollment to re-assess eligibility based on ultrasound."""
    if not raw:
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(
                subject_identifier=instance.maternal_visit.subject_identifier)
            antenatal_enrollment.pending_ultrasound = False
            antenatal_enrollment.save()
        except AntenatalEnrollment.DoesNotExist:
            pass


@receiver(post_save, weak=False, sender=MaternalLabDel, dispatch_uid="maternal_lab_del_on_post_save")
def maternal_lab_del_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Update antenatal enrollment to re-assess eligibility based on delivery."""
    if not raw:
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(
                subject_identifier=instance.subject_identifier)
            antenatal_enrollment.pending_ultrasound = False
            antenatal_enrollment.save()
        except AntenatalEnrollment.DoesNotExist:
            pass
