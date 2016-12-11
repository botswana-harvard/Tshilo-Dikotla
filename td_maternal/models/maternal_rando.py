from django.db import models
from django.core.validators import RegexValidator

from edc_base.model.models import HistoricalRecords
from edc_constants.constants import NO
from edc_constants.choices import YES_NO
from django_crypto_fields.fields import EncryptedCharField

from ..choices import DELIVERY_HEALTH_FACILITY
from ..randomization import Randomization

from .maternal_crf_model import MaternalCrfModel


class MaternalRando (MaternalCrfModel):
    """ Stores a prepared infant randomization list.

    If you need to undo a randomization, here is an example of how::
        >>> # To undo a randomization
        >>> subject_identifier = '056-1980294-0'
        >>> void_sid = '222222'
        >>> # clear rando record but set to void to not allow it to be used
        >>> maternal_rando = MaternalRando.objects.get(subject_identifier=subject_identifier, sid=void_sid)
        >>> if maternal_rando:
        >>>     maternal_rando.subject_identifier='void'
        >>>     maternal_rando.randomization_datetime = None
        >>>     maternal_rando.initials = 'XX'
        >>>     maternal_rando.feeding_choice=None
        >>>     maternal_rando.infant_initials='XX'
        >>>     maternal_rando.haart_status=None
        >>>     maternal_rando.comment = "used in error by %s" % (subject_identifier,)
        >>>     maternal_rando.save()
        >>>     print "OK, SID %s is now void" % (void_sid,)
        >>>     # clear SID from registered subject
        >>>     rs = RegisteredSubject.object.get(subject_identifier=subject_identifier, sid=void_sid)
        >>>     rs.sid = None
        >>>     rs.registration_status = None
        >>>     print "OK, RegisteredSubject SID set to None"
        >>> else:
        >>>     print "Error"
"""

    ADMIN_SITE_NAME = 'td_maternal_admin'

    site = models.CharField(
        verbose_name='Site',
        max_length=15)

    sid = models.IntegerField(
        verbose_name='SID',
        unique=True)

    rx = EncryptedCharField(
        verbose_name="Treatment Assignment")

    randomization_datetime = models.DateTimeField(
        verbose_name='Randomization Datetime')

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.'))])

    dispensed = models.CharField(
        verbose_name='Dispensed',
        max_length=10,
        default=NO,
        choices=YES_NO,
        help_text='To be confirmed by pharmacy staff only')

    comment = models.TextField(
        max_length=250,
        null=True,
        blank=True,
        help_text="Comment if any manual changes made to rando list")

    delivery_clinic = models.CharField(
        max_length=100,
        verbose_name="Which clinic does the mother plan to deliver at?",
        choices=DELIVERY_HEALTH_FACILITY)

    delivery_clinic_other = models.CharField(
        max_length=100,
        verbose_name="if other delivery clinic, specify...",
        blank=True,
        null=True, )

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.sid, self.subject_identifier)

    def save(self, *args, **kwargs):
        if not self.id:
            randomization = Randomization(self)
            self.initials = randomization.initials
            self.randomization_datetime = randomization.randomization_datetime
            self.rx = randomization.rx
            self.sid = randomization.sid
            self.site = randomization.study_site
        super(MaternalRando, self).save(*args, **kwargs)

    class Meta(MaternalCrfModel.Meta):
        app_label = "td_maternal"
        verbose_name = "Maternal Randomization"
        verbose_name_plural = "Maternal Randomization"
        ordering = ('sid',)
        unique_together = ('sid', 'rx')
