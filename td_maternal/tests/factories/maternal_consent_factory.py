import factory

from datetime import date

from django.utils import timezone

from edc_constants.constants import YES, NO, FEMALE

from td_maternal.models import MaternalConsent


class MaternalConsentFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalConsent

    assessment_score = YES
    citizen = YES
    confirm_identity = "111121111"
    consent_copy = YES
    consent_datetime = timezone.now()
    consent_reviewed = YES
    consent_signature = YES
    dob = date(1988, 7, 7)
    first_name = "DIMO"
    gender = FEMALE
    identity = "111121111"
    identity_type = "OMANG"
    initials = "DD"
    is_dob_estimated = NO
    is_literate = YES
    language = 'en'
    last_name = "DIMO"
    report_datetime = timezone.now()
    study_questions = YES
    study_site = '40'
