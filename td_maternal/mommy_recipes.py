from faker import Faker
from model_mommy.recipe import Recipe, seq, foreign_key

from django.utils import timezone

from edc_base.faker import EdcBaseProvider
from edc_lab.faker import EdcLabProvider
from edc_visit_tracking.constants import SCHEDULED

from edc_constants.constants import YES, POS

from .models import MaternalConsent, MaternalVisit, MaternalEligibility, AntenatalEnrollment


class MyEdcBaseProvider(EdcBaseProvider):
    consent_model = 'td_maternal.maternalconsent'

fake = Faker()
fake.add_provider(MyEdcBaseProvider)
fake.add_provider(EdcLabProvider)


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

antenatalenrollment = Recipe(
    AntenatalEnrollment,
    schedule_name='maternal_enrollment_step1',
    current_hiv_status=POS,
    evidence_hiv_status=YES,
    rapid_test_done=None,
    rapid_test_result=None)

maternalvisit = Recipe(
    MaternalVisit,
    reason=SCHEDULED)

# maternalrequisition = Recipe(
#     MaternalRequisition,
#     requisition_identifier=edc_lab_faker.requisition_identifier,
#     specimen_type='WB',
#     is_drawn=YES)
