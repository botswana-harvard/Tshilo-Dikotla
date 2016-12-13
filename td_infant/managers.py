from django.db import models
from django.apps import apps as django_apps


class InfantDeathReportManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        return self.get(subject_identifier=subject_identifier_as_pk)


class InfantDisenrollmentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier, visit_schedule_name, schedule_name):
        return self.get(
            subject_identifier=subject_identifier,
            visit_schedule_name=visit_schedule_name, schedule_name=schedule_name)


class InfantCnsManager(models.Manager):

    def get_by_natural_key(self, cns, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(cns=cns, congenital_anomalies=infant_congenital_anomalities)


class InfantFacialDefectManager(models.Manager):

    def get_by_natural_key(self, facial_defect, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(facial_defect=facial_defect, congenital_anomalies=infant_congenital_anomalities)


class InfantCleftDisorderManager(models.Manager):

    def get_by_natural_key(self, cleft_disorder, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(cleft_disorder=cleft_disorder, congenital_anomalies=infant_congenital_anomalities)


class InfantMouthUpGiManager(models.Manager):

    def get_by_natural_key(self, mouth_up_gi, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(mouth_up_gi=mouth_up_gi, congenital_anomalies=infant_congenital_anomalities)


class InfantCardioDisorderManager(models.Manager):

    def get_by_natural_key(self, cardio_disorder, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(cardio_disorder=cardio_disorder, congenital_anomalies=infant_congenital_anomalities)


class InfantRespiratoryDefectManager(models.Manager):

    def get_by_natural_key(self, respiratory_defect, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(respiratory_defect=respiratory_defect, congenital_anomalies=infant_congenital_anomalities)


class InfantLowerGiManager(models.Manager):

    def get_by_natural_key(self, lower_gi, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(lower_gi=lower_gi, congenital_anomalies=infant_congenital_anomalities)


class InfantFemaleGenitalManager(models.Manager):

    def get_by_natural_key(self, female_genital, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(female_genital=female_genital, congenital_anomalies=infant_congenital_anomalities)


class InfantMaleGenitalManager(models.Manager):

    def get_by_natural_key(self, male_genital, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(male_genital=male_genital, congenital_anomalies=infant_congenital_anomalities)


class InfantRenalManager(models.Manager):

    def get_by_natural_key(self, InfantRenal, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(InfantRenal=InfantRenal, congenital_anomalies=infant_congenital_anomalities)


class InfantMusculoskeletalManager(models.Manager):

    def get_by_natural_key(self, musculo_skeletal, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(musculo_skeletal=musculo_skeletal, congenital_anomalies=infant_congenital_anomalities)


class InfantSkinManager(models.Manager):

    def get_by_natural_key(self, skin, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(skin=skin, congenital_anomalies=infant_congenital_anomalities)


class InfantTrisomiesManager(models.Manager):

    def get_by_natural_key(self, trisomies, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(trisomies=trisomies, congenital_anomalies=infant_congenital_anomalities)


class InfantOtherAbnormalityItemsManager(models.Manager):

    def get_by_natural_key(self, other_abnormalities, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantCongenitalAnomalies = django_apps.get_model('td_infant', 'InfantCongenitalAnomalies')
        infant_congenital_anomalities = InfantCongenitalAnomalies.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(other_abnormalities=other_abnormalities, congenital_anomalies=infant_congenital_anomalities)


class InfantArvProphModManager(models.Manager):

    def get_by_natural_key(self, arv_code, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantArvProph = django_apps.get_model('td_infant', 'InfantArvProph')
        infant_arv_proph = InfantArvProph.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(arv_codefu_dx=arv_code, infant_arv_proph=infant_arv_proph)


class InfantBirthModelManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class InfantFuDxItemsManager(models.Manager):

    def get_by_natural_key(self, fu_dx, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantFuDx = django_apps.get_model('td_infant', 'InfantFuDxItems')
        infant_fu_dx = InfantFuDx.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(fu_dx=fu_dx, congenital_anomalies=infant_fu_dx)


class VaccinesMissedManager(models.Manager):

    def get_by_natural_key(self, received_vaccine_name, report_datetime,
                           visit_instance, code, subject_identifier_as_pk):
        InfantFuImmunizations = django_apps.get_model('td_infant', 'InfantFuImmunizations')
        infant_fu_immunizations = InfantFuImmunizations.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(received_vaccine_name=received_vaccine_name, infant_fu_immunizations=infant_fu_immunizations)


class VaccinesReceivedManager(models.Manager):

    def get_by_natural_key(self, missed_vaccine_name, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantFuImmunizations = django_apps.get_model('td_infant', 'InfantFuImmunizations')
        infant_fu_immunizations = InfantFuImmunizations.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(missed_vaccine_name=missed_vaccine_name, infant_fu_immunizations=infant_fu_immunizations)


class InfantFuNewMedItemsManager(models.Manager):

    def get_by_natural_key(self, medication, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantFuNewMed = django_apps.get_model('td_infant', 'InfantFuNewMed')
        infant_fu_med = InfantFuNewMed.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(medication=medication, infant_fu_med=infant_fu_med)


class InfantVaccinesManager(models.Manager):

    def get_by_natural_key(self, vaccination, report_datetime, visit_instance, code, subject_identifier_as_pk):
        InfantVaccines = django_apps.get_model('td_infant', 'InfantFuNewMed')
        infant_birth_feed_vaccine = InfantVaccines.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(vaccination=vaccination, infant_birth_feed_vaccine=infant_birth_feed_vaccine)
