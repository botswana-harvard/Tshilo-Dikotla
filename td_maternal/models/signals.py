from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_constants.constants import ALIVE, ON_STUDY
from edc_identifier.maternal_identifier import MaternalIdentifier, MaternalIdentifierError
from edc_visit_tracking.constants import SCHEDULED

from td.models import Appointment

from .antenatal_enrollment import AntenatalEnrollment
from .maternal_consent import MaternalConsent
from .maternal_eligibility import MaternalEligibility
from .maternal_labour_del import MaternalLabourDel
from .maternal_offstudy import MaternalOffstudy
from .maternal_visit import MaternalVisit


@receiver(post_save, weak=False, sender=MaternalEligibility, dispatch_uid="maternal_eligibility_on_post_save")
def maternal_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw and not kwargs.get('update_fields'):
        instance.create_update_or_delete_eligibility_loss()


@receiver(post_save, sender=MaternalConsent, dispatch_uid="maternalconsent_on_post_save")
def maternal_consent_on_post_save(sender, instance, raw, **kwargs):
    if not raw:
        instance.registration_update_or_create()


@receiver(post_save, sender=AntenatalEnrollment, weak=False, dispatch_uid="ineligible_take_off_study")
def ineligible_take_off_study(sender, instance, raw, created, using, **kwargs):
    """If not is_eligible, sets to off study."""
    if not raw:
        try:
            if not instance.is_eligible and not instance.pending_ultrasound:
                instance.take_off_study()
        except AttributeError as e:
            if 'is_eligible' not in str(e) and 'pending_ultrasound' not in str(e):
                raise AttributeError(str(e))


def put_back_on_study_from_failed_eligibility(instance):
    """Attempts to change the 1000M maternal visit back to scheduled
    from off study."""
    with transaction.atomic():
        try:
            appointment = Appointment.objects.get(
                subject_identifier=instance.registered_subject.subject_identifier,
                visit_code='1000M')
            maternal_visit = MaternalVisit.objects.get(
                appointment=appointment)
            maternal_visit.study_status = ON_STUDY
            maternal_visit.reason = SCHEDULED
            maternal_visit.save()
        except MaternalVisit.DoesNotExist:
            MaternalVisit.objects.create(
                appointment=appointment,
                report_datetime=instance.report_datetime,
                survival_status=ALIVE,
                study_status=ON_STUDY,
                reason=SCHEDULED)
        except Appointment.DoesNotExist:
            pass


@receiver(post_save, weak=False, dispatch_uid="eligible_put_back_on_study")
def eligible_put_back_on_study(sender, instance, raw, created, using, **kwargs):
    """changes the 1000M visit to scheduled from off study if is_eligible."""
    if not raw:
        try:
            if isinstance(instance, AntenatalEnrollment) and (instance.pending_ultrasound or instance.is_eligible):
                MaternalOffstudy.objects.get(
                    maternal_visit__appointment__subject_identifier=instance.registered_subject)
        except AttributeError as e:
            if 'is_eligible' not in str(e) and 'registered_subject' not in str(e):
                raise
        except MaternalOffstudy.DoesNotExist:
            put_back_on_study_from_failed_eligibility(instance)


# @receiver(post_save, weak=False, dispatch_uid="maternal_ultrasound_delivery_initial_on_post_save")
# def maternal_ultrasound_delivery_initial_on_post_save(sender, instance, raw, created, using, **kwargs):
#     """Update antenatal enrollment to indicate if eligibility is passed on not based on ultra sound form results."""
#     if not raw:
#         if isinstance(instance, MaternalUltraSoundInitial) or isinstance(instance, MaternalLabourDel):
#             # re-save antenatal enrollment record to recalculate eligibility
#             antenatal_enrollment = instance.antenatal_enrollment
#             antenatal_enrollment.pending_ultrasound = False
#             antenatal_enrollment.save()


@receiver(post_save, weak=False, sender=MaternalLabourDel, dispatch_uid='create_infant_identifier_on_labour_delivery')
def create_infant_identifier_on_labour_delivery(sender, instance, raw, created, using, **kwargs):
    """Creates an identifier for the registered infant.

    Only one infant per mother is allowed."""
    if not raw and created:
        if instance.live_infants_to_register == 1:
            maternal_identifier = MaternalIdentifier(identifier=instance.subject_identifier)
            try:
                maternal_identifier.deliver(
                    1, model=sender._meta.label_lower,
                    create_registration=True,
                    registration_datetime=instance.delivery_datetime,
                    user_created=instance.user_created)
            except MaternalIdentifierError:
                pass
