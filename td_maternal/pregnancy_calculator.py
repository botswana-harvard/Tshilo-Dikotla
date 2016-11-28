from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow

LMP = 0
ULTRASOUND = 1


class Lmp:

    def __init__(self, lmp=None, reference_date=None):
        self.date = lmp
        self.reference_date = reference_date or get_utcnow()
        try:
            self.edd = self.date + relativedelta(days=280)
            self.ga = relativedelta(weeks=40) - relativedelta(self.edd - self.reference_date)
        except TypeError:
            self.edd = None
            self.ga = None


class Ultrasound:

    def __init__(self, ultrasound_date=None, ga_weeks=None, ga_days=None):
        self.date = None
        self.edd = None
        self.ga = None
        if ultrasound_date:
            self.date = ultrasound_date
            if ga_weeks is not None:
                if not 0 < ga_weeks < 40:
                    raise TypeError('Invalid Ultrasound GA weeks, expected 0 < ga_weeks < 40. Got {}'.format(ga_weeks))
            ga_days = ga_days or 0
            if not 0 <= ga_days <= 6:
                raise TypeError('Invalid Ultrasound GA days, expected 0 <= ga_days <= 6. Got {}'.format(ga_days))
            try:
                self.ga = relativedelta(weeks=ga_weeks) + relativedelta(days=ga_days)
            except TypeError:
                pass
            if self.ga:
                self.edd = self.date + self.ga


class Ga:
    def __init__(self, lmp, ultrasound):
        self.ultrasound = ultrasound or Ultrasound()
        try:
            lmp = lmp.date
        except AttributeError:
            pass
        self.lmp = Lmp(lmp=lmp, reference_date=self.ultrasound.date)
        self.ga = self.lmp.ga or ultrasound.ga


class Edd:

    def __init__(self, lmp=None, ultrasound=None):
        self.edd = None
        self.edd_confirmation_method = None
        self.lmp = lmp or Lmp()
        self.ultrasound = ultrasound or Ultrasound()
        self.edd_confirmation_method = None
        try:
            self.edd = self.get_edd(relativedelta(days=abs(relativedelta(self.lmp.edd - self.ultrasound.date).days)))
        except TypeError as e:
            if self.lmp.edd:
                self.edd = self.lmp.edd
                self.edd_confirmation_method = LMP
            elif self.ultrasound.edd:
                self.edd = self.ultrasound.edd
                self.edd_confirmation_method = ULTRASOUND
            elif not self.lmp.edd and not self.ultrasound.edd:
                pass
            else:
                raise TypeError(str(e))

    def get_edd(self, delta):
        edd = None
        if relativedelta(weeks=16) <= self.lmp.ga <= relativedelta(weeks=21) + relativedelta(days=6):
            if 0 <= delta.days <= 10:
                edd = self.lmp.edd
                self.edd_confirmation_method = LMP
            elif 10 < delta.days:
                edd = self.ultrasound.edd
                self.edd_confirmation_method = ULTRASOUND
        elif (relativedelta(weeks=21) + relativedelta(days=6) < self.lmp.ga <=
              relativedelta(weeks=27) + relativedelta(days=6)):
            if 0 <= delta.days <= 14:
                edd = self.lmp.edd
                self.edd_confirmation_method = LMP
            elif 14 < delta.days:
                edd = self.ultrasound.edd
                self.edd_confirmation_method = ULTRASOUND
        elif relativedelta(weeks=27) + relativedelta(days=6) < self.lmp.ga:
            if 0 <= delta.days <= 21:
                edd = self.lmp.edd
                self.edd_confirmation_method = LMP
            elif 21 < delta.days:
                edd = self.ultrasound.edd
                self.edd_confirmation_method = ULTRASOUND
        return edd
