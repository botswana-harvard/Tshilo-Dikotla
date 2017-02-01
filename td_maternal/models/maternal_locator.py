from django.db import models
from django.utils import timezone

# from edc_base.audit_trail import AuditTrail
    
from django_crypto_fields.fields import EncryptedCharField
from edc_appointment.models import Appointment
from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import (CellNumber, TelephoneNumber,
    datetime_not_before_study_start, datetime_not_future)
from edc_constants.choices import YES_NO
from edc_export.models import ExportTrackingFieldsMixin
from edc_locator.models import LocatorMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_registration.models import RegisteredSubject


from .maternal_visit import MaternalVisit


class LocalCrfMetaDataManager(CrfMetaDataManager):

    def create_meta_data(self):
        if self.visit_instance.appointment.visit_definition.code == '1000M':
            super(LocalCrfMetaDataManager, self).create_meta_data()
        else:
            pass


class MaternalLocator(LocatorMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user to capture locator information and
    the details of the infant caretaker. """

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    # appointment = models.ForeignKey(Appointment, null=True)
    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=timezone.now,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    care_clinic = OtherCharField(
        verbose_name="Health clinic where your infant will receive their routine care ",
        max_length=35,
    )

    has_caretaker = models.CharField(
        verbose_name=(
            "Has the participant identified someone who will be "
            "responsible for the care of the baby in case of her death, to whom the "
            "study team could share information about her baby's health?"),
        max_length=25,
        choices=YES_NO,
        help_text="")

    caretaker_name = EncryptedCharField(
        verbose_name="Full Name of the responsible person",
        max_length=35,
        help_text="include firstname and surname",
        blank=True,
        null=True)

    caretaker_cell = EncryptedCharField(
        verbose_name="Cell number",
        max_length=8,
        validators=[CellNumber, ],
        blank=True,
        null=True)

    caretaker_tel = EncryptedCharField(
        verbose_name="Telephone number",
        max_length=8,
        validators=[TelephoneNumber, ],
        blank=True,
        null=True)

    entry_meta_data_manager = LocalCrfMetaDataManager(MaternalVisit)

    class Meta:
        app_label = 'td_maternal'
        verbose_name = 'Maternal Locator'
        verbose_name_plural = 'Maternal Locator'
