from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_constants.constants import (
    FEMALE, SCHEDULED, SCREENED, CONSENTED, FAILED_ELIGIBILITY, ALIVE, OFF_STUDY, ON_STUDY)

from .maternal_consent import MaternalConsent
from .maternal_eligibility import MaternalEligibility
from .maternal_eligibility_loss import MaternalEligibilityLoss


@receiver(post_save, weak=False, dispatch_uid="maternal_eligibility_on_post_save")
def maternal_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Creates/Updates RegisteredSubject and creates or deletes MaternalEligibilityLoss

    If participant is consented, does nothing

    * If registered subject does not exist, it will be created and some attrs
      updated from the MaternalEligibility;
    * If registered subject already exists will update some attrs from the MaternalEligibility;
    * If registered subject and consent already exist, does nothing.

    Note: This is the ONLY place RegisteredSubject is created for mothers in this project."""
    if not raw:
        if isinstance(instance, MaternalEligibility) and not kwargs.get('update_fields'):
            if not instance.is_eligible:
                try:
                    maternal_eligibility_loss = MaternalEligibilityLoss.objects.get(
                        maternal_eligibility_id=instance.id)
                    maternal_eligibility_loss.report_datetime = instance.report_datetime
                    maternal_eligibility_loss.reason_ineligible = instance.ineligibility
                    maternal_eligibility_loss.user_modified = instance.user_modified
                    maternal_eligibility_loss.save()
                except MaternalEligibilityLoss.DoesNotExist:
                    MaternalEligibilityLoss.objects.create(
                        maternal_eligibility_id=instance.id,
                        report_datetime=instance.report_datetime,
                        reason_ineligible=instance.ineligibility,
                        user_created=instance.user_created,
                        user_modified=instance.user_modified)
            else:
                MaternalEligibilityLoss.objects.filter(maternal_eligibility_id=instance.id).delete()
                try:
                    registered_subject = RegisteredSubject.objects.get(
                        screening_identifier=instance.eligibility_id,
                        subject_type='maternal')
                    MaternalConsent.objects.get(registered_subject=registered_subject)
                except RegisteredSubject.DoesNotExist:
                    registered_subject = create_maternal_registered_subject(instance)
                    instance.registered_subject = registered_subject
                    instance.save()
                except MaternalConsent.DoesNotExist:
                    registered_subject = update_maternal_registered_subject(registered_subject, instance)
                    registered_subject.save()


def create_maternal_registered_subject(instance):
    return RegisteredSubject.objects.create(
        created=instance.created,
        first_name='Mother',
        gender=FEMALE,
        registration_status=SCREENED,
        screening_datetime=instance.report_datetime,
        screening_identifier=instance.eligibility_id,
        screening_age_in_years=instance.age_in_years,
        subject_type='maternal',
        user_created=instance.user_created)


def update_maternal_registered_subject(registered_subject, instance):
    registered_subject.first_name = 'Mother'
    registered_subject.gender = FEMALE
    registered_subject.registration_status = SCREENED
    registered_subject.screening_datetime = instance.report_datetime
    registered_subject.screening_identifier = instance.eligibility_id
    registered_subject.screening_age_in_years = instance.age_in_years
    registered_subject.subject_type = 'maternal'
    registered_subject.user_modified = instance.user_modified
    return registered_subject


@receiver(post_save, weak=False, dispatch_uid="maternal_consent_on_post_save")
def maternal_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Update maternal_eligibility consented flag and consent fields on registered subject."""
    if not raw:
        if isinstance(instance, MaternalConsent):
            maternal_eligibility = MaternalEligibility.objects.get(
                registered_subject=instance.registered_subject)
            maternal_eligibility.is_consented = True
            maternal_eligibility.save(update_fields=['is_consented'])
            instance.registered_subject.registration_datetime = instance.consent_datetime
            instance.registered_subject.registration_status = CONSENTED
            instance.registered_subject.save(update_fields=['registration_datetime', 'registration_status'])
