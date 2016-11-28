from dateutil.relativedelta import relativedelta


class Lmp:

    def __init__(self, lmp):
        self.lmp = lmp
        self.edd = self.lmp + relativedelta(days=280)


class Ultrasound:

    def __init__(self, dt, ga_weeks, ga_days=0):
        ga_days = ga_days or 0
        if not 0 <= ga_days <= 7:
            raise TypeError('Invalid Ultrasound GA days, expected 0 <= ga_days <= 7. Got {}'.format(ga_days))
        self.date = dt
        if not 0 < ga_weeks < 40:
            raise TypeError('Invalid Ultrasound GA weeks, expected 0 < ga_weeks < 40. Got {}'.format(ga_weeks))
        self.ga = relativedelta(weeks=ga_weeks) + relativedelta(days=ga_days)
        self.edd = self.date + (relativedelta(weeks=40) - self.ga).weeks


class Edd:

    def __init__(self, lmp, ultrasound):
        self.final = None
        self.ultrasound = ultrasound
        self.lmp = lmp
        try:
            self.edd = self.get_edd(relativedelta(days=abs(self.lmp.edd - self.ultrasound.date)))
        except AttributeError:
            self.edd = None

    def get_edd(self, diff):
        edd = None
        diff = relativedelta(days=abs(self.lmp.edd - self.ultrasound.date))
        if relativedelta(weeks=16) <= self.lmp.ga <= relativedelta(weeks=21) + relativedelta(days=6):
            if 0 <= diff.days <= 10:
                edd = self.lmp.edd
            elif 10 < self.diff.days:
                edd = self.ultrasound.edd
        elif relativedelta(weeks=21) + relativedelta(days=6) < self.lmp.ga <= relativedelta(weeks=27) + relativedelta(days=6):
            if 0 <= diff.days <= 14:
                edd = self.lmp.edd
            elif 14 < self.diff.days:
                edd = self.ultrasound.edd
        elif relativedelta(weeks=27) + relativedelta(days=6) < self.lmp.ga:
            if 0 <= diff.days <= 21:
                edd = self.lmp.edd
            elif 21 < self.diff.days:
                edd = self.ultrasound.edd
        return edd
