from edc_pregnancy_utils import Lmp, Ga, Ultrasound, Edd

from .models import AntenatalEnrollment, MaternalUltraSoundInitial, MaternalLabDel


class Pregnancy:

    def __init__(self, subject_identifier, reference_datetime):
        self.delivery_datetime = None
        self.edd = Edd()
        self.ga = Ga(lmp=Lmp(), ultrasound=Ultrasound())
        self.ga_by_lmp = None
        self.reference_datetime = reference_datetime
        self.subject_identifier = subject_identifier
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
            try:
                maternal_lab_del = MaternalLabDel.objects.get(
                    subject_identifier=self.subject_identifier,
                    delivery_datetime__lte=self.reference_datetime)
                self.delivery_datetime = maternal_lab_del.delivery_datetime
            except MaternalLabDel.DoesNotExist:
                self.delivery_datetime = None
            lmp = Lmp(
                lmp=antenatal_enrollment.last_period_date,
                reference_date=(self.delivery_datetime or self.reference_datetime).date())
            try:
                maternal_ultrasound = MaternalUltraSoundInitial.objects.get(
                    maternal_visit__subject_identifier=self.subject_identifier)
                ultrasound = Ultrasound(
                    ultrasound_date=maternal_ultrasound.report_datetime.date(),
                    ga_confirmed_weeks=maternal_ultrasound.ga_by_ultrasound_wks,
                    ga_confirmed_days=maternal_ultrasound.ga_by_ultrasound_days,
                    ultrasound_edd=maternal_ultrasound.est_edd_ultrasound)
            except MaternalUltraSoundInitial.DoesNotExist:
                ultrasound = Ultrasound()
            self.ga_by_lmp = antenatal_enrollment.ga_lmp_enrollment_wks
            self.ga = Ga(lmp, ultrasound, prefer_ultrasound=True)
            self.edd = Edd(lmp=lmp, ultrasound=ultrasound)
        except AntenatalEnrollment.DoesNotExist:
            pass
