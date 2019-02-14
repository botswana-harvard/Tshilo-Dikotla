from edc_constants.constants import NOT_REQUIRED, REQUIRED, ADDITIONAL, NOT_ADDITIONAL
from edc_visit_schedule.classes.visit_schedule_configuration import RequisitionPanelTuple, CrfTuple


maternal_enrollment_entries = (
    #CrfTuple(10, 'td_maternal', 'maternallocator', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternalultrasoundinitial',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalobstericalhistory',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalmedicalhistory',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternaldemographics',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternallifetimearvhistory',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(70, 'td_maternal', 'maternalarvpreg', NOT_REQUIRED, ADDITIONAL),
    CrfTuple(80, 'td_maternal', 'maternalclinicalmeasurementsone',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(90, 'td_maternal', 'maternaloffstudy', NOT_REQUIRED, ADDITIONAL))

maternal_antenatal1_entries = (
    #CrfTuple(20, 'td_maternal', 'maternalultrasoundfu', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternalultrasoundinitial',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalrando', NOT_REQUIRED, ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalinterimidcc',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalclinicalmeasurementstwo',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'rapidtestresult', NOT_REQUIRED, ADDITIONAL),
)

maternal_antenatal2_entries = (
    #CrfTuple(20, 'td_maternal', 'maternalultrasoundfu', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalarvpreg', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalinterimidcc',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternaldiagnoses', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternalsubstanceusepriorpreg',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(70, 'td_maternal', 'maternalclinicalmeasurementstwo',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(80, 'td_maternal', 'rapidtestresult', NOT_REQUIRED, ADDITIONAL),
)

maternal_birth_entries = (
    CrfTuple(20, 'td_maternal', 'maternaldiagnoses', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalhivinterimhx',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalarvpreg', NOT_REQUIRED, ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalinterimidcc',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(
        60, 'td_maternal', 'maternalsubstanceuseduringpreg', REQUIRED, ADDITIONAL),
    CrfTuple(70, 'td_maternal', 'rapidtestresult', NOT_REQUIRED, ADDITIONAL),
)

maternal_followup1month_entries = (
    CrfTuple(20, 'td_maternal', 'maternalpostpartumfu',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalpostpartumdep',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalarvpost', NOT_REQUIRED, ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalarvpostadh',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternalinterimidcc',
             NOT_REQUIRED, ADDITIONAL),
    CrfTuple(70, 'td_maternal', 'rapidtestresult', NOT_REQUIRED, ADDITIONAL),
    CrfTuple(80, 'td_maternal', 'maternalclinicalmeasurementstwo',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(90, 'td_maternal', 'maternalcontraception',
             REQUIRED, NOT_ADDITIONAL),
)

maternal_followup1_entries = maternal_followup1month_entries + (
    CrfTuple(100, 'td_maternal', 'maternalsrh', NOT_REQUIRED, ADDITIONAL),
)

maternal_followup2_entries = (
    CrfTuple(20, 'td_maternal', 'maternalpostpartumfu',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalpostpartumdep',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalarvpost', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalarvpostadh',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternalinterimidcc',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(70, 'td_maternal', 'maternalclinicalmeasurementstwo',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(80, 'td_maternal', 'maternalcontraception',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(90, 'td_maternal', 'rapidtestresult', NOT_REQUIRED, ADDITIONAL),
    CrfTuple(100, 'td_maternal', 'maternalsrh', NOT_REQUIRED, ADDITIONAL),
)


maternal_followup3_entries = (
    CrfTuple(20, 'td_maternal', 'maternalpostpartumfu',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalarvpost', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalarvpostadh',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalinterimidcc',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternalclinicalmeasurementstwo',
             REQUIRED, NOT_ADDITIONAL),
)

maternal_followup24_months_entries = maternal_followup3_entries + (
    CrfTuple(70, 'td_maternal', 'maternalcontraception',
             REQUIRED, NOT_ADDITIONAL),
    CrfTuple(80, 'td_maternal', 'maternalsrh', NOT_REQUIRED, ADDITIONAL),
)


maternal_requisition_antenatal1 = (
    RequisitionPanelTuple(
        10, 'td_lab', 'maternalrequisition',
        'CD4', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        20, 'td_lab', 'maternalrequisition',
        'PBMC VL', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        30, 'td_lab', 'maternalrequisition',
        'Fasting Glucose', 'TEST', 'WB', REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        40, 'td_lab', 'maternalrequisition',
        'Glucose 1h', 'TEST', 'WB', REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        50, 'td_lab', 'maternalrequisition',
        'Glucose 2h', 'TEST', 'WB', REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        60, 'td_lab', 'maternalrequisition',
        'PBMC Plasma (STORE ONLY)', 'TEST', 'WB', REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        70, 'td_lab', 'maternalrequisition',
        'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
)

maternal_requisition_antenatal2 = (
    RequisitionPanelTuple(
        10, 'td_lab', 'maternalrequisition',
        'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        20, 'td_lab', 'maternalrequisition',
        'CD4', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        30, 'td_lab', 'maternalrequisition',
        'Fasting Glucose', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        40, 'td_lab', 'maternalrequisition',
        'Glucose 1h', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        50, 'td_lab', 'maternalrequisition',
        'Glucose 2h', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
)

maternal_requisition_followup = (
    RequisitionPanelTuple(
        10, 'td_lab', 'maternalrequisition',
        'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        20, 'td_lab', 'maternalrequisition',
        'CD4', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        30, 'td_lab', 'maternalrequisition',
        'Fasting Glucose', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        40, 'td_lab', 'maternalrequisition',
        'Glucose 1h', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        50, 'td_lab', 'maternalrequisition',
        'Glucose 2h', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
)

maternal_requisition_followup_2000M = maternal_requisition_followup + (
    RequisitionPanelTuple(
        60, 'td_lab', 'maternalrequisition',
        'PBMC VL', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
)
