from django.db import models
from django.apps import apps as django_apps

from edc_consent.managers import ConsentManager

from edc_registration.models import RegisteredSubject
from edc_visit_tracking.managers import CrfModelManager


class AntenatalEnrollmentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(registered_subject=registered_subject)


class MaternalLifetimeArvHistoryManager(models.Manager):

    def get_by_natural_key(self, report_datetime, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(report_datetime=report_datetime, registered_subject=registered_subject)


class MaternalArvManager(models.Manager):

    def get_by_natural_key(self, arv_code, start_date, report_datetime, visit_instance, code, subject_identifier_as_pk):
        MaternalArvPreg = django_apps.get_model('td_maternal', 'MaternalArvPreg')
        maternal_arv_preg = MaternalArvPreg.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(arv_code=arv_code, start_date=start_date, maternal_arv_preg=maternal_arv_preg)


class MaternalArvPostModManager(models.Manager):

    def get_by_natural_key(
            self, arv_code, modification_date, report_datetime, visit_instance, appt_status,
            visit_definition_code, subject_identifier_as_pk):
        MaternalVisit = django_apps.get_model('td_maternal', 'MaternalVisit')
        MaternalArvPost = django_apps.get_model('td_maternal', 'MaternalArvPost')
        maternal_visit = MaternalVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, appt_status, visit_definition_code, subject_identifier_as_pk)
        maternal_arv_post = MaternalArvPost.objects.get(maternal_visit=maternal_visit)
        return self.get(arv_code=arv_code, modification_date=modification_date, maternal_arv_post=maternal_arv_post)


class MaternalArvPregManager(models.Manager):

    def get_by_natural_key(self, report_datetime, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(report_datetime=report_datetime, registered_subject=registered_subject)


class MaternalAztNvpManager(models.Manager):

    def get_by_natural_key(self, azt_nvp, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(azt_nvp=azt_nvp, registered_subject=registered_subject)


class MaternalClinicalMeasurementsManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(registered_subject=registered_subject)


class MaternalConsentManager(ConsentManager):

    def get_by_natural_key(self, subject_identifier, first_name, dob, initials, version):
        return self.get(subject_identifier, first_name, dob, initials, version)


class MaternalEligibilityLossManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        MaternalEligibility = django_apps.get_model('td_maternal', 'MaternalEligibility')
        maternal_eligibility = MaternalEligibility.objects.get_by_natural_key(eligibility_id=eligibility_id)
        return self.get(maternal_eligibility=maternal_eligibility)


class MaternalEligibilityManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        return self.get(eligibility_id=eligibility_id)


class MaternalLabDelDxTManager(models.Manager):

    def get_by_natural_key(self, lab_del_dx, report_datetime, visit_instance,
                           appt_status, visit_definition_code, subject_identifier_as_pk):
        MaternalVisit = django_apps.get_model('td_maternal', 'MaternalVisit')
        MaternalLabDelDx = django_apps.get_model('td_maternal', 'MaternalLabDelDx')
        maternal_visit = MaternalVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, appt_status, visit_definition_code, subject_identifier_as_pk)
        maternal_lab_del_dx = MaternalLabDelDx.objects.get(maternal_visit=maternal_visit)
        return self.get(lab_del_dx=lab_del_dx, maternal_lab_del_dx=maternal_lab_del_dx)


class MaternalLabourDelManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(registered_subject=registered_subject)


class MaternalRandoManager(models.Manager):

    def get_by_natural_key(self, sid, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(sid=sid, registered_subject=registered_subject)


class RapidTestResultManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(registered_subject=registered_subject)


class SpecimenConsentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(registered_subject=registered_subject)


class VisitCrfModelManager(CrfModelManager):

    def get_by_natural_key(self, report_datetime, visit_instance, visit_code, subject_identifier_as_pk):
        MaternalVisit = django_apps.get_model('td_maternal', 'MaternalVisit')
        maternal_visit = MaternalVisit.objects.get_by_natural_key(report_datetime,
                                                                  visit_instance,
                                                                  visit_code,
                                                                  subject_identifier_as_pk)
        return self.get(maternal_visit=maternal_visit)
