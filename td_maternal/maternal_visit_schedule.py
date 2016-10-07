from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_schedule.visit_schedule import VisitSchedule
from edc_visit_schedule.visit import Crf, Requisition
from edc_visit_schedule.schedule import Schedule

from .td_maternal_lab_profiles import (pbmc_vl_panel, pbmc_panel, fasting_glucose_panel,
                                       glucose_1h_panel, glucose_2h_panel, hiv_elisa_panel, cd4_panel)

maternal_requisition_antenatal1 = (
    Requisition(show_order=10, model='td_maternal.maternalrequisition', panel=cd4_panel),
    Requisition(show_order=20, model='td_maternal.maternalrequisition', panel=pbmc_vl_panel),
    Requisition(show_order=30, model='td_maternal.maternalrequisition', panel=pbmc_panel),
    Requisition(show_order=40, model='td_maternal.maternalrequisition', panel=fasting_glucose_panel),
    Requisition(show_order=50, model='td_maternal.maternalrequisition', panel=glucose_1h_panel),
    Requisition(show_order=60, model='td_maternal.maternalrequisition', panel=glucose_2h_panel),
)

maternal_requisition_antenatal2 = (
    Requisition(show_order=10, model='td_maternal.maternalrequisition', panel=hiv_elisa_panel),
)

maternal_requisition_followup = (
    Requisition(show_order=10, model='td_maternal.maternalrequisition', panel=pbmc_vl_panel),
)

maternal_enrollment_crfs = (
    Crf(show_order=10, model='td_maternal.maternallocator'),
    Crf(show_order=20, model='td_maternal.maternalultrasoundinitial'),
    Crf(show_order=30, model='td_maternal.maternalobstericalhistory'),
    Crf(show_order=40, model='td_maternal.maternalmedicalhistory'),
    Crf(show_order=50, model='td_maternal.maternaldemographics'),
    Crf(show_order=60, model='td_maternal.maternallifetimearvhistory'),
    Crf(show_order=70, model='td_maternal.maternalarvpreg'),
    Crf(show_order=80, model='td_maternal.maternalclinicalmeasurementsone'),
    Crf(show_order=90, model='td_maternal.maternaloffstudy'),
)

maternal_antenatal1_crfs = (
    Crf(show_order=10, model='td_maternal.maternalultrasoundinitial'),
    Crf(show_order=20, model='td_maternal.maternalrando'),
    Crf(show_order=30, model='td_maternal.maternalinterimidcc'),
    Crf(show_order=40, model='td_maternal.maternalclinicalmeasurementstwo'),
    Crf(show_order=50, model='td_maternal.rapidtestresult'),
)

maternal_antenatal2_crfs = (
    Crf(show_order=10, model='td_maternal.maternalaztnvp'),
    Crf(show_order=20, model='td_maternal.maternalinterimidcc'),
    Crf(show_order=30, model='td_maternal.maternaldiagnoses'),
    Crf(show_order=40, model='td_maternal.maternalsubstanceusepriorpreg'),
    Crf(show_order=50, model='td_maternal.maternalclinicalmeasurementstwo'),
    Crf(show_order=60, model='td_maternal.rapidtestresult'),
)

maternal_birth_crfs = (
    Crf(show_order=10, model='td_maternal.maternaldiagnoses'),
    Crf(show_order=20, model='td_maternal.maternalhivinterimhx'),
    Crf(show_order=30, model='td_maternal.maternalarvpreg'),
    Crf(show_order=40, model='td_maternal.maternalinterimidcc'),
    Crf(show_order=50, model='td_maternal.maternalsubstanceuseduringpreg'),
    Crf(show_order=60, model='td_maternal.rapidtestresult'),
)

maternal_followup1_crfs = (
    Crf(show_order=10, model='td_maternal.maternalpostpartumfu'),
    Crf(show_order=20, model='td_maternal.maternalpostpartumdep'),
    Crf(show_order=30, model='td_maternal.maternalarvpost'),
    Crf(show_order=40, model='td_maternal.maternalarvpostadh'),
    Crf(show_order=50, model='td_maternal.maternalinterimidcc'),
    Crf(show_order=60, model='td_maternal.rapidtestresult'),
    Crf(show_order=70, model='td_maternal.maternalclinicalmeasurementstwo'),
    Crf(show_order=80, model='td_maternal.maternalcontraception'),
)

maternal_followup2_crfs = (
    Crf(show_order=10, model='td_maternal.maternalpostpartumfu'),
    Crf(show_order=20, model='td_maternal.maternalpostpartumdep'),
    Crf(show_order=30, model='td_maternal.maternalarvpost'),
    Crf(show_order=40, model='td_maternal.maternalarvpostadh'),
    Crf(show_order=50, model='td_maternal.maternalinterimidcc'),
)

maternal_followup3_crfs = (
    Crf(show_order=10, model='td_maternal.maternalpostpartumfu'),
    Crf(show_order=20, model='td_maternal.maternalpostpartumdep'),
    Crf(show_order=30, model='td_maternal.maternalarvpost'),
    Crf(show_order=40, model='td_maternal.maternalarvpostadh'),
    Crf(show_order=50, model='td_maternal.maternalinterimidcc'),
)

maternal_visit_schedule = VisitSchedule(
    name='maternal_visit_schedule',
    verbose_name='Maternal Visit Schedule',
    app_label='td_maternal',
    visit_model='td_maternal.maternalvisit',
)

# antenatal enrollment schedule
maternal_antenatal_enrollment = Schedule(
    name='maternal_antenatal_enrollment',
    enrollment_model='td_maternal.antenatalenrollment')

maternal_antenatal_enrollment.add_visit(
    code='1000M',
    title='Maternal Enrollment Visit',
    timepoint=0,
    base_interval=0,
    requisitions=None,
    crfs=maternal_enrollment_crfs
)
maternal_visit_schedule.add_schedule(maternal_antenatal_enrollment)

# antenatal visit 1 and 2 schedule
maternal_antenatal_schedule = Schedule(
    name='maternal_antenatal_schedule',
    enrollment_model='td_maternal.antenatalvisitmembership')

maternal_antenatal_schedule.add_visit(
    code='1010M',
    title='Antenatal Visit 1',
    timepoint=0,
    base_interval=0,
    requisitions=maternal_requisition_antenatal1,
    crfs=maternal_antenatal1_crfs
)

maternal_antenatal_schedule.add_visit(
    code='1020M',
    title='Antenatal Visit 2',
    timepoint=1,
    base_interval=1,
    requisitions=maternal_requisition_antenatal2,
    crfs=maternal_antenatal2_crfs
)
maternal_visit_schedule.add_schedule(maternal_antenatal_schedule)

# follow up visit
follow_up_visit_schedule = Schedule(
    name='Follow up visit schedule',
    enrollment_model='td_maternal.maternallabourdel')

follow_up_visit_schedule.add_visit(
    code='2000M',
    title='Delivery Visit',
    timepoint=0,
    base_interval=0,
    requisitions=maternal_requisition_followup,
    crfs=maternal_birth_crfs)

follow_up_visit_schedule.add_visit(
    code='2010M',
    title='1 Month Visit',
    timepoint=1,
    base_interval=1,
    requisitions=maternal_requisition_followup,
    crfs=maternal_followup1_crfs)

follow_up_visit_schedule.add_visit(
    code='2020M',
    title='2 Months Visit',
    timepoint=2,
    base_interval=2,
    requisitions=maternal_requisition_followup,
    crfs=maternal_followup1_crfs)

follow_up_visit_schedule.add_visit(
    code='2060M',
    title='6 Months Visit',
    timepoint=3,
    base_interval=3,
    requisitions=maternal_requisition_followup,
    crfs=maternal_followup1_crfs)

follow_up_visit_schedule.add_visit(
    code='2120M',
    title='12 Months Visit',
    timepoint=4,
    base_interval=4,
    requisitions=maternal_requisition_followup,
    crfs=maternal_followup2_crfs)

follow_up_visit_schedule.add_visit(
    code='2180M',
    title='18 Months Visit',
    timepoint=5,
    base_interval=5,
    requisitions=maternal_requisition_followup,
    crfs=maternal_followup3_crfs)

follow_up_visit_schedule.add_visit(
    code='2240M',
    title='24 Months Visit',
    timepoint=6,
    base_interval=6,
    requisitions=maternal_requisition_followup,
    crfs=maternal_followup3_crfs)

follow_up_visit_schedule.add_visit(
    code='2300M',
    title='30 Months Visit',
    timepoint=7,
    base_interval=7,
    requisitions=maternal_requisition_followup,
    crfs=maternal_followup3_crfs)

follow_up_visit_schedule.add_visit(
    code='2360M',
    title='36 Months Visit',
    timepoint=8,
    base_interval=8,
    requisitions=maternal_requisition_followup,
    crfs=maternal_followup3_crfs)
maternal_visit_schedule.add_schedule(follow_up_visit_schedule)
