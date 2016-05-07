from collections import OrderedDict

from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleTuple)

from ..models import SpecimenConsent


class SpecimenConsentVisitSchedule(VisitScheduleConfiguration):

    name = 'specimen visit schedule'

    app_label = 'mb_maternal'

    membership_forms = OrderedDict({
        'specimen': MembershipFormTuple('specimen', SpecimenConsent, True)
    })

    schedules = OrderedDict({
        'Specimen Consent': ScheduleTuple('Specimen Consent', 'specimen', None, None)
    })

    visit_definitions = OrderedDict()

site_visit_schedules.register(SpecimenConsentVisitSchedule)
