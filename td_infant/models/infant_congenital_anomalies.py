from django.db import models

from edc_base.model.fields import OtherCharField
# from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_constants.choices import CONFIRMED_SUSPECTED
from edc_visit_tracking.models import CrfInlineModelMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_sync.models import SyncModelMixin, SyncHistoricalRecords

from tshilo_dikotla.choices import (
    CNS_ABNORMALITIES, FACIAL_DEFECT, CLEFT_DISORDER, MOUTH_UP_GASTROINT_DISORDER,
    CARDIOVASCULAR_DISORDER, RESPIRATORY_DEFECT, LOWER_GASTROINTESTINAL_ABNORMALITY,
    FEM_GENITAL_ANOMALY, MALE_GENITAL_ANOMALY, RENAL_ANOMALY, MUSCULOSKELETAL_ABNORMALITY,
    SKIN_ABNORMALITY, TRISOME_CHROSOMESOME_ABNORMALITY, OTHER_DEFECT)

from ..managers import (InfantCnsManager, InfantFacialDefectManager,
                        InfantCleftDisorderManager, InfantMouthUpGiManager, InfantOtherAbnormalityItemsManager,
                        InfantCardioDisorderManager, InfantRespiratoryDefectManager, InfantLowerGiManager,
                        InfantFemaleGenitalManager, InfantMaleGenitalManager, InfantRenalManager,
                        InfantMusculoskeletalManager, InfantSkinManager, InfantTrisomiesManager)

from .infant_crf_model import InfantCrfModel


class InfantCongenitalAnomalies(InfantCrfModel):

    """ A model completed by the user on the infant's congenital anomalies. """

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies"


class BaseCnsItem(CrfInlineModelMixin, SyncModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    history = SyncHistoricalRecords()

    class Meta:
        abstract = True


class InfantCns(BaseCnsItem):

    cns = models.CharField(
        max_length=250,
        choices=CNS_ABNORMALITIES,
        verbose_name="Central nervous system abnormality",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    cns_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantCnsManager()

    def natural_key(self):
        return (self.cns, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies:Cns"
        unique_together = ('cns', 'congenital_anomalies')


class InfantFacialDefect(BaseCnsItem):

    facial_defect = models.CharField(
        max_length=250,
        choices=FACIAL_DEFECT,
        verbose_name="Facial defects",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    facial_defects_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantFacialDefectManager()

    def natural_key(self):
        return (self.facial_defect, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies:Facial"
        unique_together = ('facial_defect', 'congenital_anomalies')


class InfantCleftDisorder(BaseCnsItem):

    cleft_disorder = models.CharField(
        max_length=250,
        choices=CLEFT_DISORDER,
        verbose_name="Cleft disorders",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    cleft_disorders_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantCleftDisorderManager()

    def natural_key(self):
        return (self.cleft_disorder, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies:Cleft"
        unique_together = ('cleft_disorder', 'congenital_anomalies')


class InfantMouthUpGi(BaseCnsItem):

    mouth_up_gi = models.CharField(
        max_length=250,
        choices=MOUTH_UP_GASTROINT_DISORDER,
        verbose_name="Mouth and upper gastrointestinal disorders",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    mouth_up_gi_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True
    )

    objects = InfantMouthUpGiManager()

    def natural_key(self):
        return (self.mouth_up_gi, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies:MouthUp"
        unique_together = ('mouth_up_gi', 'congenital_anomalies')


class InfantCardioDisorder(BaseCnsItem):

    cardio_disorder = models.CharField(
        max_length=250,
        choices=CARDIOVASCULAR_DISORDER,
        verbose_name="Cardiovascular disorders",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    cardiovascular_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantCardioDisorderManager()

    def natural_key(self):
        return (self.cardio_disorder, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies:Cardio"
        unique_together = ('cardio_disorder', 'congenital_anomalies')


class InfantRespiratoryDefect(BaseCnsItem):

    respiratory_defect = models.CharField(
        max_length=250,
        choices=RESPIRATORY_DEFECT,
        verbose_name="Respiratory defects",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    respiratory_defects_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantRespiratoryDefectManager()

    def natural_key(self):
        return (self.respiratory_defect, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies:Respiratory"
        unique_together = ('respiratory_defect', 'congenital_anomalies')


class InfantLowerGi(BaseCnsItem):

    lower_gi = models.CharField(
        max_length=250,
        choices=LOWER_GASTROINTESTINAL_ABNORMALITY,
        verbose_name="Lower gastrointestinal abnormalities",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    lower_gi_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify",
        blank=True,
        null=True,
    )

    objects = InfantLowerGiManager()

    def natural_key(self):
        return (self.lower_gi, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies:Lower GI"
        unique_together = ('lower_gi', 'congenital_anomalies')


class InfantFemaleGenital(BaseCnsItem):

    female_genital = models.CharField(
        max_length=250,
        choices=FEM_GENITAL_ANOMALY,
        verbose_name="Female genital anomaly",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    female_genital_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantFemaleGenitalManager()

    def natural_key(self):
        return (self.female_genital, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies:Female Gen"
        unique_together = ('female_genital', 'congenital_anomalies')


class InfantMaleGenital(BaseCnsItem):

    male_genital = models.CharField(
        max_length=250,
        choices=MALE_GENITAL_ANOMALY,
        verbose_name="Male genital anomaly",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    male_genital_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantMaleGenitalManager()

    def natural_key(self):
        return (self.male_genital, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies:Male Gen"
        unique_together = ('male_genital', 'congenital_anomalies')


class InfantRenal(BaseCnsItem):

    renal = models.CharField(
        max_length=250,
        choices=RENAL_ANOMALY,
        verbose_name="Renal anomalies",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    renal_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantRenalManager()

    def natural_key(self):
        return (self.renal, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies: Renal"
        unique_together = ('renal', 'congenital_anomalies')


class InfantMusculoskeletal(BaseCnsItem):

    musculo_skeletal = models.CharField(
        max_length=250,
        choices=MUSCULOSKELETAL_ABNORMALITY,
        verbose_name="Musculo-skeletal abnomalities",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    musculo_skeletal_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantMusculoskeletalManager()

    def natural_key(self):
        return (self.musculo_skeletal, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies: Musculo-sk"
        unique_together = ('musculo_skeletal', 'congenital_anomalies')


class InfantSkin(BaseCnsItem):

    skin = models.CharField(
        max_length=250,
        choices=SKIN_ABNORMALITY,
        verbose_name="Skin abnormalities",
        help_text="Excludes cafe au lait spots, Mongolian spots, port wine stains, "
        "nevus, hemangloma <4 cm in diameter. If hemangloma is >4 cm, specify",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    skin_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantSkinManager()

    def natural_key(self):
        return (self.skin, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies: Skin"
        unique_together = ('skin', 'congenital_anomalies')


class InfantTrisomies(BaseCnsItem):

    trisomies = models.CharField(
        max_length=250,
        choices=TRISOME_CHROSOMESOME_ABNORMALITY,
        verbose_name="Trisomies / chromosomes abnormalities",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    trisomies_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantTrisomiesManager()

    def natural_key(self):
        return (self.trisomies, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies: Trisomes"
        unique_together = ('trisomies', 'congenital_anomalies')


class InfantOtherAbnormalityItems(BaseCnsItem):

    other_abnormalities = models.CharField(
        max_length=250,
        choices=OTHER_DEFECT,
        verbose_name="Other",
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
    )

    other_abnormalities_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = InfantOtherAbnormalityItemsManager()

    def natural_key(self):
        return (self.other_abnormalities, ) + self.congenital_anomalies.natural_key()

    class Meta:
        app_label = 'td_infant'
        verbose_name = "Congenital Anomalies: Other"
        unique_together = ('other_abnormalities', 'congenital_anomalies')
