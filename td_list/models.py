from edc_base.model.models import ListModelMixin, BaseUuidModel


class AutopsyInfoSource (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Autopsy Info Source"
        verbose_name_plural = "Autopsy Info Source"


class ChronicConditions(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Chronic Conditions"
        verbose_name_plural = "Chronic Conditions"


class Contraceptives (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Contraceptives"
        verbose_name_plural = "Contraceptives"


class DeliveryComplications(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Delivery Complications"
        verbose_name_plural = "Delivery Complications"


class DiseasesAtEnrollment (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Diseases At Enrollment"
        verbose_name_plural = "Diseases At Enrollment"


class Foods (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Foods"
        verbose_name_plural = "Foods"


class HouseholdGoods (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Household Goods"
        verbose_name_plural = "Household Goods"


class InfantVaccines (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Infant Vaccines"
        verbose_name_plural = "Infant Vaccines"


class Malformations(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Fetal Malformations"
        verbose_name_plural = "Fetal Malformations"


class MaternalDiagnoses(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Diagnoses"
        verbose_name_plural = "Maternal Diagnoses"


class MaternalHospitalization(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Hospitalization"
        verbose_name_plural = "Maternal Hospitalizations"


class HealthCond (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Health Cond"


class DelComp (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Delivery Comp"


class ObComp(ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal LabDel: Ob Comp"


class MaternalMedications (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Medications"
        verbose_name_plural = "Maternal Medications"


class MaternalRelatives(ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Relatives"
        verbose_name_plural = "Maternal Relatives"


class PriorArv (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Enroll: Prior Arv"
        verbose_name_plural = "Maternal Enroll: Prior Arv"


class RandomizationItem (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Maternal Randomization Item"
        verbose_name_plural = "Maternal Randomization Item"


class Rations (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Rations"
        verbose_name_plural = "Rations"


class Supplements (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Supplements"
        verbose_name_plural = "Supplements"


class WhoAdultDiagnosis (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "WHO Adult Diagnosis"
        verbose_name_plural = "WHO Adult Diagnoses"


class WhoPedsDiagnosis (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_list'
        verbose_name = "WHO Pediatric Diagnosis"
        verbose_name_plural = "WHO Pediatric Diagnoses"
