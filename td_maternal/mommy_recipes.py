from faker import Faker
from model_mommy.recipe import Recipe, seq, foreign_key

from django.utils import timezone

from edc_base.faker import EdcBaseProvider
from edc_lab.faker import EdcLabProvider
from edc_visit_tracking.constants import SCHEDULED

from edc_constants.constants import YES, POS, NOT_APPLICABLE, NO, NEG

from .models import MaternalConsent, MaternalVisit, MaternalEligibility, AntenatalEnrollment, MaternalLabourDel
from dateutil.relativedelta import relativedelta
from faker.providers import BaseProvider


class TdProvider(BaseProvider):

    def twenty_five_weeks_ago(self):
        return timezone.now() - relativedelta(weeks=25)

    def four_weeks_ago(self):
        return timezone.now() - relativedelta(weeks=4)


class MyEdcBaseProvider(EdcBaseProvider):
    consent_model = 'td_maternal.maternalconsent'

fake = Faker()
fake.add_provider(MyEdcBaseProvider)
fake.add_provider(EdcLabProvider)
fake.add_provider(TdProvider)


maternaleligibility = Recipe(
    MaternalEligibility,
    age_in_years=25,
    has_omang=YES,)

maternalconsent = Recipe(
    MaternalConsent,
    maternal_eligibility=foreign_key(maternaleligibility),
    study_site='40',
    consent_datetime=timezone.now,
    dob=fake.dob_for_consenting_adult,
    first_name=fake.first_name,
    last_name=fake.last_name,
    initials=fake.initials,  # note, passes for model but won't pass validation in modelform clean()
    gender='M',
    identity=seq('12315678'),  # will raise IntegrityError if multiple made without _quantity
    confirm_identity=seq('12315678'),  # will raise IntegrityError if multiple made without _quantity
    identity_type='OMANG',
    is_dob_estimated='-',
)

antenatalenrollment_ineligible = Recipe(
    AntenatalEnrollment,
    schedule_name='maternal_enrollment_step1',
    report_datetime=timezone.now,
    current_hiv_status=POS,
    evidence_hiv_status=YES,
    is_diabetic=YES,
    will_breastfeed=NO,
    will_remain_onstudy=NO,
    rapid_test_done=None,
    rapid_test_result=None)

antenatalenrollment = Recipe(
    AntenatalEnrollment,
    schedule_name='maternal_enrollment_step1',
    report_datetime=timezone.now,
    current_hiv_status=YES,
    evidence_32wk_hiv_status=NOT_APPLICABLE,
    evidence_hiv_status=YES,
    is_diabetic=NO,
    knows_lmp=YES,
    last_period_date=fake.twenty_five_weeks_ago,
    rapid_test_date=fake.four_weeks_ago,
    rapid_test_done=YES,
    rapid_test_result=NEG,
    week32_test=NO,
    will_breastfeed=YES,
    will_get_arvs=NOT_APPLICABLE,
    will_remain_onstudy=YES,
)

maternalvisit = Recipe(
    MaternalVisit,
    reason=SCHEDULED)

# maternalrequisition = Recipe(
#     MaternalRequisition,
#     requisition_identifier=edc_lab_faker.requisition_identifier,
#     specimen_type='WB',
#     is_drawn=YES)

maternallabourdel = Recipe(
    MaternalLabourDel,
    report_datetime=timezone.now,
    csection_reason=NOT_APPLICABLE,
    delivery_datetime=timezone.now,
    delivery_hospital='Lesirane',
    delivery_time_estimated=NO,
    labour_hrs='3',
    live_infants_to_register=1,
    mode_delivery='spontaneous vaginal',
    valid_regiment_duration=YES)
