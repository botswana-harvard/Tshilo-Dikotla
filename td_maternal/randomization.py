from edc_base.utils import get_utcnow
from edc_constants.constants import POS

from td.constants import RANDOMIZED
from td_list.models import RandomizationItem
from td_maternal.models import MaternalConsent
from td_maternal.models.antenatal_enrollment import AntenatalEnrollment
from edc_registration.models import RegisteredSubject


class RandomizationError(Exception):
    pass


class Randomization(object):

    def __init__(self, obj, randomization_datetime=None):
        """Selects the next available record from the Pre-Populated Randomization list.

        Update the record with subject_identifier, initials and other maternal specific data.

        obj is typically a MaternalRando instance.
        """
        randomization_datetime = randomization_datetime or get_utcnow()
        self.initials = None
        self.randomization_datetime = None
        self.rx = None
        self.sid = None
        self.study_site = None
        antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=obj.subject_identifier)
        maternal_consent = MaternalConsent.objects.filter(subject_identifier=obj.subject_identifier).first()
        registered_subject = RegisteredSubject.objects.get(subject_identifier=obj.subject_identifier)
        if antenatal_enrollment.enrollment_hiv_status != POS:
            raise RandomizationError(
                "Cannot Randomize mothers that are not HIV POS. Got {}. See Antenatal Enrollment.".format(
                    antenatal_enrollment.enrollment_hiv_status))
        if obj.__class__.objects.all().count() == 0:
            next_to_pick = 1
        else:
            next_to_pick = obj.__class__.objects.all().order_by('-sid').first().sid + 1
        next_randomization_item = RandomizationItem.objects.get(name=str(next_to_pick))
        self.sid = int(next_randomization_item.name)
        self.rx = next_randomization_item.field_name
        self.initials = maternal_consent.initials
        self.randomization_datetime = randomization_datetime
        self.study_site = maternal_consent.study_site
        registered_subject.sid = self.sid
        registered_subject.randomization_datetime = randomization_datetime
        registered_subject.registration_status = RANDOMIZED
        registered_subject.modified = get_utcnow()
        registered_subject.save()
