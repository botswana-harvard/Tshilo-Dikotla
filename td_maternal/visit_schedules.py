from edc_visit_schedule.constants import MONTHS, DAYS
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_schedule.visit_schedule import VisitSchedule
from edc_visit_schedule.visit import Crf, Requisition
from edc_visit_schedule.schedule import Schedule


from .lab_profiles import (pbmc_vl_panel, pbmc_panel, fasting_glucose_panel,
                           glucose_1h_panel, glucose_2h_panel, hiv_elisa_panel, cd4_panel)

visit_schedule = VisitSchedule(
    name='maternal_visit_schedule',
    verbose_name='Maternal Visit Schedule',
    app_label='td_maternal',
    death_report_model='td_maternal.maternaldeathreport',
    default_disenrollment_model='td_maternal.maternaldisenrollment',
    default_enrollment_model=None,
    offstudy_model='td_maternal.maternaloffstudy',
    visit_model='td_maternal.maternalvisit',
)

# requisitions
requisition_antenatal1 = (
    Requisition(show_order=10, model='td_lab.maternalrequisition', panel=cd4_panel),
    Requisition(show_order=20, model='td_lab.maternalrequisition', panel=pbmc_vl_panel),
    Requisition(show_order=30, model='td_lab.maternalrequisition', panel=pbmc_panel),
    Requisition(show_order=40, model='td_lab.maternalrequisition', panel=fasting_glucose_panel),
    Requisition(show_order=50, model='td_lab.maternalrequisition', panel=glucose_1h_panel),
    Requisition(show_order=60, model='td_lab.maternalrequisition', panel=glucose_2h_panel),
)

requisition_antenatal2 = (
    Requisition(show_order=10, model='td_lab.maternalrequisition', panel=hiv_elisa_panel),
)

requisition_followup = (
    Requisition(show_order=10, model='td_lab.maternalrequisition', panel=pbmc_vl_panel),
)

# crfs
enrollment_crfs = (
    Crf(show_order=10, model='td_maternal.maternallocator'),
    Crf(show_order=20, model='td_maternal.maternalultrasoundinitial'),
    Crf(show_order=30, model='td_maternal.maternalobstericalhistory'),
    Crf(show_order=40, model='td_maternal.maternalmedicalhistory'),
    Crf(show_order=50, model='td_maternal.maternaldemographics'),
    Crf(show_order=60, model='td_maternal.maternallifetimearvhistory'),
    Crf(show_order=70, model='td_maternal.maternalarvpreg'),
    Crf(show_order=80, model='td_maternal.maternalclinicalmeasurementsone'),
    Crf(show_order=90, model='td_maternal.maternaloffstudy', required=False),
)

antenatal1_crfs = (
    Crf(show_order=10, model='td_maternal.maternalultrasoundinitial'),
    Crf(show_order=20, model='td_maternal.maternalrando'),
    Crf(show_order=30, model='td_maternal.maternalinterimidcc'),
    Crf(show_order=40, model='td_maternal.maternalclinicalmeasurementstwo'),
    Crf(show_order=50, model='td_maternal.rapidtestresult'),
)

antenatal2_crfs = (
    Crf(show_order=10, model='td_maternal.maternalinterimidcc'),
    Crf(show_order=20, model='td_maternal.maternaldiagnoses'),
    Crf(show_order=30, model='td_maternal.maternalsubstanceusepriorpreg'),
    Crf(show_order=40, model='td_maternal.maternalclinicalmeasurementstwo'),
    Crf(show_order=50, model='td_maternal.rapidtestresult'),
)

delivery_crfs = (
    Crf(show_order=10, model='td_maternal.maternaldiagnoses'),
    Crf(show_order=20, model='td_maternal.maternalhivinterimhx'),
    Crf(show_order=30, model='td_maternal.maternalarvpreg'),
    Crf(show_order=40, model='td_maternal.maternalinterimidcc'),
    Crf(show_order=50, model='td_maternal.maternalsubstanceuseduringpreg'),
    Crf(show_order=60, model='td_maternal.rapidtestresult'),
    Crf(show_order=70, model='td_maternal.nvpdispensing'),
)

followup1_crfs = (
    Crf(show_order=10, model='td_maternal.maternalpostpartumfu'),
    Crf(show_order=20, model='td_maternal.maternalpostpartumdep'),
    Crf(show_order=30, model='td_maternal.maternalarvpost'),
    Crf(show_order=40, model='td_maternal.maternalarvpostadh'),
    Crf(show_order=50, model='td_maternal.maternalinterimidcc'),
    Crf(show_order=60, model='td_maternal.rapidtestresult'),
    Crf(show_order=70, model='td_maternal.maternalclinicalmeasurementstwo'),
    Crf(show_order=80, model='td_maternal.maternalcontraception'),
)

followup2_crfs = (
    Crf(show_order=10, model='td_maternal.maternalpostpartumfu'),
    Crf(show_order=20, model='td_maternal.maternalpostpartumdep'),
    Crf(show_order=30, model='td_maternal.maternalarvpost'),
    Crf(show_order=40, model='td_maternal.maternalarvpostadh'),
    Crf(show_order=50, model='td_maternal.maternalinterimidcc'),
)

followup3_crfs = (
    Crf(show_order=10, model='td_maternal.maternalpostpartumfu'),
    Crf(show_order=20, model='td_maternal.maternalpostpartumdep'),
    Crf(show_order=30, model='td_maternal.maternalarvpost'),
    Crf(show_order=40, model='td_maternal.maternalarvpostadh'),
    Crf(show_order=50, model='td_maternal.maternalinterimidcc'),
)

# antenatal enrollment schedule
antenatal_enrollment1 = Schedule(
    name='maternal_enrollment_step1',
    enrollment_model='td_maternal.antenatalenrollment')

antenatal_enrollment1.add_visit(
    code='1000M',
    title='Maternal Enrollment Visit',
    timepoint=0,
    base_interval=0,
    base_interval_unit=DAYS,
    requisitions=(),
    crfs=enrollment_crfs
)

# antenatal schedule
antenatal_enrollment2 = Schedule(
    name='maternal_enrollment_step2',
    enrollment_model='td_maternal.antenatalenrollmenttwo')


antenatal_enrollment2.add_visit(
    code='1010M',
    title='Antenatal Visit 1',
    timepoint=0,
    base_interval=0,
    base_interval_unit=DAYS,
    requisitions=requisition_antenatal1,
    crfs=antenatal1_crfs
)

antenatal_enrollment2.add_visit(
    code='1020M',
    title='Antenatal Visit 2',
    timepoint=1,
    base_interval=3,
    base_interval_unit=MONTHS,
    requisitions=requisition_antenatal2,
    crfs=antenatal2_crfs
)

# follow up visit
follow_up = Schedule(
    name='follow_up',
    enrollment_model='td_maternal.maternallabdel')

follow_up.add_visit(
    code='2000M',
    title='Delivery Visit',
    timepoint=0,
    base_interval=0,
    base_interval_unit=MONTHS,
    requisitions=requisition_followup,
    crfs=delivery_crfs)

follow_up.add_visit(
    code='2010M',
    title='1 Month Visit',
    timepoint=1,
    base_interval=1,
    base_interval_unit=MONTHS,
    requisitions=requisition_followup,
    crfs=followup1_crfs)

follow_up.add_visit(
    code='2020M',
    title='2 Months Visit',
    timepoint=2,
    base_interval=2,
    base_interval_unit=MONTHS,
    requisitions=requisition_followup,
    crfs=followup1_crfs)

follow_up.add_visit(
    code='2060M',
    title='6 Months Visit',
    timepoint=3,
    base_interval=6,
    base_interval_unit=MONTHS,
    requisitions=requisition_followup,
    crfs=followup1_crfs)

follow_up.add_visit(
    code='2120M',
    title='12 Months Visit',
    timepoint=4,
    base_interval=12,
    base_interval_unit=MONTHS,
    requisitions=requisition_followup,
    crfs=followup2_crfs)

follow_up.add_visit(
    code='2180M',
    title='18 Months Visit',
    timepoint=5,
    base_interval=18,
    base_interval_unit=MONTHS,
    requisitions=requisition_followup,
    crfs=followup3_crfs)

follow_up.add_visit(
    code='2240M',
    title='24 Months Visit',
    timepoint=6,
    base_interval=24,
    base_interval_unit=MONTHS,
    requisitions=requisition_followup,
    crfs=followup3_crfs)

follow_up.add_visit(
    code='2300M',
    title='30 Months Visit',
    timepoint=7,
    base_interval=30,
    base_interval_unit=MONTHS,
    requisitions=requisition_followup,
    crfs=followup3_crfs)

follow_up.add_visit(
    code='2360M',
    title='36 Months Visit',
    timepoint=8,
    base_interval=36,
    base_interval_unit=MONTHS,
    requisitions=requisition_followup,
    crfs=followup3_crfs)

# add schedules
visit_schedule.add_schedule(antenatal_enrollment1)
visit_schedule.add_schedule(antenatal_enrollment2)
visit_schedule.add_schedule(follow_up)

# register
site_visit_schedules.register(visit_schedule)
