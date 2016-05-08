from edc_visit_schedule.classes.visit_schedule_configuration import RequisitionPanelTuple, CrfTuple
from edc_constants.constants import NOT_REQUIRED, REQUIRED, ADDITIONAL, NOT_ADDITIONAL


maternal_antenatal_entries = (
    CrfTuple(10, 'td_maternal', 'maternalultrasound', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, 'td_maternal', 'maternaloffstudy', NOT_REQUIRED, ADDITIONAL))

# maternal_delivery_entries = (
#     CrfTuple(10L, 'td_maternal', 'maternallabourdel', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(20L, 'td_maternal', 'maternallabdelmed', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(30L, 'td_maternal', 'maternallabdelclinic', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(40L, 'td_maternal', 'maternallabdeldx', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(45L, 'td_maternal', 'maternalheightweight', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(48L, 'td_maternal', 'maternalbreasthealth', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(50L, 'td_maternal', 'maternalarvpreg', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(70L, 'td_maternal', 'maternalbreasthealth', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(80L, 'td_maternal', 'maternalpostfumed', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(100L, 'td_maternal', 'maternaldeathreport', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(110L, 'td_maternal', 'maternaloffstudy', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(120L, 'td_maternal', 'reproductivehealth', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(130L, 'td_maternal', 'maternalsrh', NOT_REQUIRED, ADDITIONAL))
# 
# maternal_monthly_entries = (
#     CrfTuple(10L, 'td_maternal', 'maternalpostf', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(20L, 'td_maternal', 'maternalpostfudx', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(25L, 'td_maternal', 'maternalpostfumed', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(30L, 'td_maternal', 'reproductivehealth', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(40L, 'td_maternal', 'maternalsrh', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(50L, 'td_maternal', 'maternalarvpost', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(60L, 'td_maternal', 'maternalarvpostadh', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(70L, 'td_maternal', 'maternalbreasthealth', REQUIRED, NOT_ADDITIONAL),
#     CrfTuple(90L, 'td_maternal', 'rapidtestresult', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(200L, 'td_maternal', 'maternaldeathreport', NOT_REQUIRED, ADDITIONAL),
#     CrfTuple(210L, 'td_maternal', 'maternaloffstudy', NOT_REQUIRED, ADDITIONAL))

maternal_requisition_entries = (
    RequisitionPanelTuple(
        10L, 'td_lab', 'maternalrequisition',
        'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        20L, 'td_lab', 'maternalrequisition',
        'Breast Milk (Storage)', 'STORAGE', 'BM', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        30L, 'td_lab', 'maternalrequisition',
        'Vaginal swab (Storage)', 'STORAGE', 'VS', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        40L, 'td_lab', 'maternalrequisition',
        'Rectal swab (Storage)', 'STORAGE', 'RS', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        50L, 'td_lab', 'maternalrequisition',
        'Skin Swab (Storage)', 'STORAGE', 'SW', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        60L, 'td_lab', 'maternalrequisition',
        'Vaginal STI Swab (Storage)', 'TEST', 'VS', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        70L, 'td_lab', 'maternalrequisition',
        'Hematology (ARV)', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
    RequisitionPanelTuple(
        80L, 'td_lab', 'maternalrequisition',
        'CD4/ CD8', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
)
