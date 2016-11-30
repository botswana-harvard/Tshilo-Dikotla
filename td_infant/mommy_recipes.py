from dateutil.relativedelta import relativedelta

from faker.providers import BaseProvider

from model_mommy.recipe import Recipe

from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NOT_APPLICABLE, NO

from td.constants import MODIFIED

from .models import (InfantBirth, InfantBirthData, InfantBirthExam, InfantFeeding, InfantBirthArv, InfantFu,
                     InfantFuPhysical, InfantArvProph)


class TdProvider(BaseProvider):

    def thirty_four_weeks_ago(self):
        return (get_utcnow() - relativedelta(weeks=34)).date()

    def twenty_five_weeks_ago(self):
        return (get_utcnow() - relativedelta(weeks=25)).date()

    def four_weeks_ago(self):
        return (get_utcnow() - relativedelta(weeks=4)).date()

infantbirth = Recipe(
    InfantBirth,
    report_datetime=get_utcnow,
    first_name='BABY',
    initials='BB',
    dob=get_utcnow,
    gender='F',)

infantbirthdata = Recipe(
    InfantBirthData,
    report_datetime=get_utcnow(),
    weight_kg=3.61,
    infant_length=89.97,
    head_circumference=39.30,
    apgar_score=NO,
    congenital_anomalities=NO)

infantbirthexam = Recipe(
    InfantBirthExam,
    report_datetime=get_utcnow(),
    infant_exam_date=get_utcnow().date(),
    general_activity='NORMAL',
    physical_exam_result='NORMAL',
    heent_exam=YES,
    resp_exam=YES,
    cardiac_exam=YES,
    abdominal_exam=YES,
    skin_exam=YES,
    neurologic_exam=YES,
    other_exam_info='NA')

infantfeeding = Recipe(
    InfantFeeding,
    report_datetime=get_utcnow(),
    other_feeding=YES,
    formula_intro_occur=YES,
    formula_intro_date=get_utcnow().date(),
    took_formula=YES,
    is_first_formula=YES,
    date_first_formula=get_utcnow().date(),
    est_date_first_formula=YES,
    water=YES,
    juice=YES,
    cow_milk=YES,
    cow_milk_yes='boiled',
    other_milk=NO,
    milk_boiled=NOT_APPLICABLE,
    fruits_veg=NO,
    cereal_porridge=NO,
    solid_liquid=YES,
    rehydration_salts=NO,
    water_used='Water direct from source',
    ever_breastfeed=YES,
    complete_weaning=NOT_APPLICABLE,
    weaned_completely=NO,
    times_breastfed='<1 per week',)

infantbirtharv = Recipe(
    InfantBirthArv,
    report_datetime=get_utcnow(),
    azt_after_birth=NO,
    azt_additional_dose=NO,
    sdnvp_after_birth=NO,
    azt_discharge_supply=NO,)

infantfollowup = Recipe(
    InfantFu,
    report_datetime=get_utcnow(),
    physical_assessment=NO,
    diarrhea_illness=NO,
    has_dx=NO,
    was_hospitalized=NO,)

infantfollowup = Recipe(
    InfantFuPhysical,
    report_datetime=get_utcnow(),
    weight_kg=3,
    height=45.01,
    head_circumference=18.01,
    general_activity="NORMAL",
    physical_exam_result="NORMAL",
    heent_exam=YES,
    was_hospitalized=YES,
    resp_exam=YES,
    cardiac_exam=YES,
    abdominal_exam=YES,
    skin_exam=YES,
    neurologic_exam=YES,)

infantfollowup = Recipe(
    InfantArvProph,
    report_datetime=get_utcnow(),
    prophylatic_nvp=YES,
    arv_status=MODIFIED,)
