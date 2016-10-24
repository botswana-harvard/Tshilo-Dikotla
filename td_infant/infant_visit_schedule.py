from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_schedule.visit_schedule import VisitSchedule
from edc_visit_schedule.visit import Crf, Requisition
from edc_visit_schedule.schedule import Schedule

from td_infant.td_infant_lab_profiles import (
    infant_birth_pbmc_pl_panel, infant_glucose_panel, infant_birth_insulin_panel,
    infant_pp1_heu_pbmc_pl_panel, infant_pp1_huu_pbmc_pl_panel, infant_pp1_insulin_panel,
    infant_heelstick_panel, infant_pp18_huu_pbmc_pl_panel, infant_pp18_heu_insulin_panel,
    infant_pp18_huu_insulin_panel, infant_pp36_pbmc_pl_panel, infant_pp36_insulin_panel)


infant_birth_requisitions = (
    Requisition(show_order=10, model='td_lab.infantrequisition', panel=infant_birth_pbmc_pl_panel),
    Requisition(show_order=20, model='td_lab.infantrequisition', panel=infant_glucose_panel),
    Requisition(show_order=30, model='td_lab.infantrequisition', panel=infant_birth_insulin_panel),
)

infant_1month_requisitions = (
    Requisition(show_order=10, model='td_lab.infantrequisition', panel=infant_pp1_heu_pbmc_pl_panel),
    Requisition(show_order=20, model='td_lab.infantrequisition', panel=infant_pp1_huu_pbmc_pl_panel),
    Requisition(show_order=30, model='td_lab.infantrequisition', panel=infant_pp1_insulin_panel),
)

infant_pp2_heelstick_requisition = (
    Requisition(show_order=10, model='td_lab.infantrequisition', panel=infant_heelstick_panel),
)

infant_18month_requisitions = (
    Requisition(show_order=10, model='td_lab.infantrequisition', panel=infant_pp18_huu_pbmc_pl_panel),
    Requisition(show_order=20, model='td_lab.infantrequisition', panel=infant_pp18_heu_insulin_panel),
    Requisition(show_order=30, model='td_lab.infantrequisition', panel=infant_pp18_huu_insulin_panel),
)

infant_36month_requisitions = (
    Requisition(show_order=10, model='td_lab.infantrequisition', panel=infant_pp36_pbmc_pl_panel),
    Requisition(show_order=20, model='td_lab.infantrequisition', panel=infant_pp36_insulin_panel),
    Requisition(show_order=30, model='td_lab.infantrequisition', panel=infant_glucose_panel),
)

infant_birth_crf = (
    Crf(show_order=10, model='td_infant.infantbirthdata'),
    Crf(show_order=20, model='td_infant.infantbirthexam'),
    Crf(show_order=30, model='td_infant.infantbirthfeedingvaccine'),
    Crf(show_order=40, model='td_infant.infantbirtharv'),
    Crf(show_order=50, model='td_infant.infantcongenitalanomalies'),
    Crf(show_order=60, model='td_infant.infantdeathreport'),
)

infant_1month_visit_crfs = (
    Crf(show_order=10, model='td_infant.infantfu'),
    Crf(show_order=20, model='td_infant.infantfuphysical'),
    Crf(show_order=30, model='td_infant.infantfudx'),
    Crf(show_order=40, model='td_infant.infantfunewmed'),
    Crf(show_order=50, model='td_infant.infantarvproph'),
    Crf(show_order=60, model='td_infant.infantfeeding'),
)

infant_2month_visit_crfs = (
    Crf(show_order=10, model='td_infant.infantfu'),
    Crf(show_order=20, model='td_infant.infantfuphysical'),
    Crf(show_order=30, model='td_infant.infantfudx'),
    Crf(show_order=40, model='td_infant.infantfunewmed'),
    Crf(show_order=50, model='td_infant.infantfuimmunizations'),
    Crf(show_order=60, model='td_infant.infantarvproph'),
    Crf(show_order=70, model='td_infant.infantfeeding'),
)

infant_followup_crfs = (
    Crf(show_order=10, model='td_infant.infantfu'),
    Crf(show_order=20, model='td_infant.infantfuphysical'),
    Crf(show_order=30, model='td_infant.infantfudx'),
    Crf(show_order=40, model='td_infant.infantfunewmed'),
    Crf(show_order=50, model='td_infant.infantarvproph'),
    Crf(show_order=60, model='td_infant.infantfeeding'),
    Crf(show_order=70, model='td_infant.solidfoodassessment'),
)


infant_visit_schedule = VisitSchedule(
    name='infant_visit_schedule',
    verbose_name='Infant Birth Visit Schedule',
    app_label='td_infant',
    visit_model='td_infant.infantvisit',
)

infant_birth_schedule = Schedule(
    name='Infant Enrollment',
    enrollment_model='td_infant.infantbirth')

infant_birth_schedule.add_visit(
    code='2000',
    title='Birth',
    timepoint=0,
    base_interval=0,
    requisitions=infant_birth_requisitions,
    crfs=infant_birth_crf
)

infant_birth_schedule.add_visit(
    code='2010',
    title='Infant 1 Month Visit',
    timepoint=1,
    base_interval=1,
    requisitions=infant_1month_requisitions,
    crfs=infant_1month_visit_crfs
)

infant_birth_schedule.add_visit(
    code='2020',
    title='Infant 2 Month Visit',
    timepoint=2,
    base_interval=2,
    requisitions=infant_pp2_heelstick_requisition,
    crfs=infant_2month_visit_crfs
)

infant_birth_schedule.add_visit(
    code='2060',
    title='Infant 6 Month Visit',
    timepoint=3,
    base_interval=3,
    requisitions=infant_pp2_heelstick_requisition,
    crfs=infant_followup_crfs)

infant_birth_schedule.add_visit(
    code='2120',
    title='Infant 12 Month Visit',
    timepoint=4,
    base_interval=4,
    requisitions=None,
    crfs=infant_followup_crfs)

infant_birth_schedule.add_visit(
    code='2180',
    title='Infant 18 Month Visit',
    timepoint=5,
    base_interval=5,
    requisitions=infant_18month_requisitions,
    crfs=infant_followup_crfs)

infant_birth_schedule.add_visit(
    code='2240',
    title='Infant 24 Month Visit',
    timepoint=6,
    base_interval=6,
    requisitions=None,
    crfs=infant_followup_crfs)

infant_birth_schedule.add_visit(
    code='2300',
    title='Infant 30 Month Visit',
    timepoint=7,
    base_interval=7,
    requisitions=None,
    crfs=infant_followup_crfs)

infant_birth_schedule.add_visit(
    code='2360',
    title='Infant 36 Month Visit',
    timepoint=8,
    base_interval=8,
    requisitions=infant_36month_requisitions,
    crfs=infant_followup_crfs)
infant_visit_schedule.add_schedule(infant_birth_schedule)

site_visit_schedules.register(infant_visit_schedule)
