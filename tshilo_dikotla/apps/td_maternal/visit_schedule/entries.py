from edc_visit_schedule.classes.visit_schedule_configuration import RequisitionPanelTuple, CrfTuple
from edc_constants.constants import NOT_REQUIRED, REQUIRED, ADDITIONAL, NOT_ADDITIONAL


maternal_enrollment_entries = (
    CrfTuple(10, 'td_maternal', 'maternallocator', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternalultrasoundinitial', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalobstericalhistory', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalmedicalhistory', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternaldemographics', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternallifetimearvhistory', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(70, 'td_maternal', 'maternalarvpreg', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(80, 'td_maternal', 'maternalclinicalmeasurementsone', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(90, 'td_maternal', 'maternaloffstudy', REQUIRED, NOT_ADDITIONAL))

maternal_antenatal1_entries = (
    CrfTuple(10, 'td_maternal', 'maternallocator', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternalultrasoundfu', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalrando', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalinterimidcc', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalclinicalmeasurementstwo', REQUIRED, NOT_ADDITIONAL),
)

maternal_antenatal2_entries = (
    CrfTuple(10, 'td_maternal', 'maternallocator', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternalultrasoundfu', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalaztnvp', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalinterimidcc', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternaldiagnoses', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternalclinicalmeasurementstwo', REQUIRED, NOT_ADDITIONAL),
)

maternal_birth_entries = (
    CrfTuple(10, 'td_maternal', 'maternallocator', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternaldiagnoses', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'Maternalhivinterimhx', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalarvpreg', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalinterimidcc', REQUIRED, NOT_ADDITIONAL),
)

maternal_followup1_entries = (
    CrfTuple(10, 'td_maternal', 'maternallocator', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternalpostpartumfu', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalpostpartumdep', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalarvpost', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalarvpostadh', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternalinterimidcc', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(70, 'td_maternal', 'rapidtestresult', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(80, 'td_maternal', 'maternalclinicalmeasurementstwo', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(90, 'td_maternal', 'maternalcontraception', REQUIRED, NOT_ADDITIONAL),
)

maternal_followup2_entries = (
    CrfTuple(10, 'td_maternal', 'maternallocator', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternalpostpartumfu', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalpostpartumdep', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalarvpost', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalarvpostadh', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternalinterimidcc', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(60, 'td_maternal', 'maternalweight', REQUIRED, NOT_ADDITIONAL),
)

maternal_followup3_entries = (
    CrfTuple(10, 'td_maternal', 'maternallocator', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternalpostpartumfu', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(30, 'td_maternal', 'maternalpostpartumdep', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(40, 'td_maternal', 'maternalarvpost', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(50, 'td_maternal', 'maternalarvpostadh', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(60, 'td_maternal', 'maternalinterimidcc', REQUIRED, NOT_ADDITIONAL),
)

maternal_requisition_antenatal1 = (
    RequisitionPanelTuple(
        10, 'td_lab', 'maternalrequisition',
        'CD4', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        20, 'td_lab', 'maternalrequisition',
        'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
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
        20, 'td_lab', 'maternalrequisition',
        'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
)