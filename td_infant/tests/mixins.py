from model_mommy import mommy

from td.models import Appointment


class MaternalMixin:

    def create_mother(self):
        maternal_eligibility = mommy.make_recipe('td_maternal.maternaleligibility')
        maternal_consent = mommy.make_recipe(
            'td_maternal.maternalconsent',
            maternal_eligibility_reference=maternal_eligibility.reference)
        subject_identifier = maternal_consent.subject_identifier
        mommy.make_recipe(
            'td_maternal.antenatalenrollment',
            subject_identifier=subject_identifier)
        appointment = Appointment.objects.get(
            subject_identifier=subject_identifier, visit_code='1000M')
        maternal_visit_1000 = mommy.make_recipe(
            'td_maternal.maternalvisit', appointment=appointment, reason='scheduled')
        mommy.make_recipe(
            'td_maternal.maternalultrasoundinitial', maternal_visit=maternal_visit_1000, number_of_gestations=1)
        mommy.make_recipe(
            'td_maternal.antenatalenrollmenttwo',
            subject_identifier=subject_identifier)
        return subject_identifier
