from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_schedule.visit_schedule import VisitSchedule
from edc_visit_schedule.visit import Crf, Requisition
from edc_visit_schedule.schedule import Schedule
from tshilo_dikotla.td_maternal_lab_profiles import (pbmc_vl_panel, pbmc_panel, fasting_glucose_panel,
                                glucose_1h_panel, glucose_2h_panel, hiv_elisa_panel, cd4_panel)


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
    Crf(show_order=50, model='td_maternal.rapidtestresult'),
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
