from django.db import models


class InfantCnsManager(models.Manager):

    def get_by_natural_key(self, cns, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(cns=cns, congenital_anomalies=infant_congenital_anomalities)


class InfantFacialDefectManager(models.Manager):

    def get_by_natural_key(self, facial_defect, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(facial_defect=facial_defect, congenital_anomalies=infant_congenital_anomalities)


class InfantCleftDisorderManager(models.Manager):

    def get_by_natural_key(self, cleft_disorder, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(cleft_disorder=cleft_disorder, congenital_anomalies=infant_congenital_anomalities)


class InfantMouthUpGiManager(models.Manager):

    def get_by_natural_key(self, mouth_up_gi, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(mouth_up_gi=mouth_up_gi, congenital_anomalies=infant_congenital_anomalities)


class InfantCardioDisorderManager(models.Manager):

    def get_by_natural_key(self, cardio_disorder, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(cardio_disorder=cardio_disorder, congenital_anomalies=infant_congenital_anomalities)


class InfantRespiratoryDefectManager(models.Manager):

    def get_by_natural_key(self, respiratory_defect, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(respiratory_defect=respiratory_defect, congenital_anomalies=infant_congenital_anomalities)


class InfantLowerGiManager(models.Manager):

    def get_by_natural_key(self, lower_gi, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(lower_gi=lower_gi, congenital_anomalies=infant_congenital_anomalities)


class InfantFemaleGenitalManager(models.Manager):

    def get_by_natural_key(self, female_genital, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(female_genital=female_genital, congenital_anomalies=infant_congenital_anomalities)


class InfantMaleGenitalManager(models.Manager):

    def get_by_natural_key(self, male_genital, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(male_genital=male_genital, congenital_anomalies=infant_congenital_anomalities)


class InfantRenalManager(models.Manager):

    def get_by_natural_key(self, InfantRenal, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(InfantRenal=InfantRenal, congenital_anomalies=infant_congenital_anomalities)


class InfantMusculoskeletalManager(models.Manager):

    def get_by_natural_key(self, musculo_skeletal, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(musculo_skeletal=musculo_skeletal, congenital_anomalies=infant_congenital_anomalities)


class InfantSkinManager(models.Manager):

    def get_by_natural_key(self, skin, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(skin=skin, congenital_anomalies=infant_congenital_anomalities)


class InfantTrisomiesManager(models.Manager):

    def get_by_natural_key(self, trisomies, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(trisomies=trisomies, congenital_anomalies=infant_congenital_anomalities)


class InfantOtherAbnormalityItemsManager(models.Manager):

    def get_by_natural_key(self, other_abnormalities, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = models.get_model('mb_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(other_abnormalities=other_abnormalities, congenital_anomalies=infant_congenital_anomalities)
