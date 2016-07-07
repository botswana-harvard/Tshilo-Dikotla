from django.db.models import Q
from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_constants.constants import POS

from tshilo_dikotla.constants import RANDOMIZED
from td_list.models import RandomizationItem
from td_maternal.models import MaternalConsent


class Randomization(object):

    def __init__(self, maternal_rando, exception_cls=None):
        self.maternal_rando = maternal_rando
        self.exception_cls = exception_cls
        self.site = None
        self.sid = None
        self.rx = None
        self.subject_identifier = None
        self.randomization_datetime = None
        self.initials = None

    def randomize(self):

        """Selects the next available record from the Pre-Populated Randomization list.
        Update the record with subject_identifier, initials and other maternal specific data."""

        self.verify_hiv_status()
#         self.verify_not_already_randomized()
        if self.maternal_rando.__class__.objects.all().count() == 0:
            next_to_pick = 1
        else:
            next_to_pick = self.maternal_rando.__class__.objects.all().order_by('-sid').first().sid + 1
        next_randomization_item = RandomizationItem.objects.get(name=str(next_to_pick))
        subject_identifier = self.maternal_rando.maternal_visit.appointment.registered_subject.subject_identifier
        consent = MaternalConsent.objects.filter(subject_identifier=subject_identifier).first()
        self.site = consent.study_site
        self.sid = int(next_randomization_item.name)
        self.rx = next_randomization_item.field_name
        self.subject_identifier = subject_identifier
        self.randomization_datetime = timezone.datetime.now()
        self.initials = self.maternal_rando.maternal_visit.appointment.registered_subject.initials

        dte = timezone.datetime.today()
        registered_subject = self.maternal_rando.maternal_visit.appointment.registered_subject
        registered_subject.sid = self.sid
        registered_subject.randomization_datetime = self.randomization_datetime
        registered_subject.modified = dte
        registered_subject.registration_status = RANDOMIZED
        registered_subject.save()
        return (self.site, self.sid, self.rx, self.subject_identifier, self.randomization_datetime, self.initials)

    def verify_hiv_status(self):
        if self.maternal_rando.antenatal_enrollment.enrollment_hiv_status != POS:
            raise self.exception_cls("Cannot Randomize mothers that are not HIV POS. Got {}. See Antenatal Enrollment."
                                     .format(self.maternal_rando.antenatal_enrollment.enrollment_hiv_status))

#     def verify_not_already_randomized(self):
#         if self.maternal_rando.maternal_visit.appointment.registered_subject.registration_status == RANDOMIZED:
#             raise self.exception_cls("Records show that this mother is already RANDOMIZED.")
