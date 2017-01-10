from edc_lab.aliquot_type import AliquotType
from edc_lab.processing_profile import ProcessingProfile
from edc_lab.lab_profile import LabProfile
from edc_lab.requisition_panel import RequisitionPanel
from edc_lab.site_labs import site_labs

lab_profile = LabProfile('td_lab')

pl = AliquotType('Plasma', 'PL', '32')
lab_profile.add_aliquot_type(pl)

bc = AliquotType('Buffy Coat', 'BC', '16')
lab_profile.add_aliquot_type(bc)

pbmc = AliquotType('PBMC', 'PBMC', '31')
lab_profile.add_aliquot_type(pbmc)

serum = AliquotType('Serum', 'SERUM', '06')
lab_profile.add_aliquot_type(serum)

wb = AliquotType('Whole Blood', 'WB', '02')
wb.add_derivative(bc)
wb.add_derivative(pl)
wb.add_derivative(pbmc)
wb.add_derivative(serum)
lab_profile.add_aliquot_type(wb)

pbmc_vl_processing = ProcessingProfile('PBMC VL', wb)
pbmc_vl_processing.add_process(pl, 4)
pbmc_vl_processing.add_process(bc, 4)
lab_profile.add_processing_profile(pbmc_vl_processing)

pbmc_processing = ProcessingProfile('PBMC Plasma (STORE ONLY)', wb)
pbmc_processing.add_process(pl, 4)
pbmc_processing.add_process(bc, 4)
lab_profile.add_processing_profile(pbmc_processing)

glucose_processing = ProcessingProfile('Glucose', wb)
glucose_processing.add_process(pl, 3)
lab_profile.add_processing_profile(glucose_processing)

elisa_processing = ProcessingProfile('ELISA', wb)
elisa_processing.add_process(pl, 1)
elisa_processing.add_process(bc, 1)
lab_profile.add_processing_profile(elisa_processing)

cd4_processing = ProcessingProfile('CD4', wb)
lab_profile.add_processing_profile(cd4_processing)

pbmc_vl_panel = RequisitionPanel('PBMC VL', wb)  # link this to the visit_schedule
pbmc_vl_panel.processing_profile = pbmc_vl_processing
lab_profile.add_panel(pbmc_vl_panel)

pbmc_panel = RequisitionPanel('PBMC Plasma (STORE ONLY)', wb)
pbmc_panel.processing_profile = pbmc_processing
lab_profile.add_panel(pbmc_panel)

fasting_glucose_panel = RequisitionPanel('Fasting Glucose', wb)
fasting_glucose_panel.processing_profile = glucose_processing
lab_profile.add_panel(fasting_glucose_panel)

glucose_1h_panel = RequisitionPanel('Glucose 1h', wb)
glucose_1h_panel.processing_profile = glucose_processing
lab_profile.add_panel(glucose_1h_panel)

glucose_2h_panel = RequisitionPanel('Glucose 2h', wb)
glucose_2h_panel.processing_profile = glucose_processing
lab_profile.add_panel(glucose_2h_panel)

hiv_elisa_panel = RequisitionPanel('HIV ELISA (PRN) ', wb)
hiv_elisa_panel.processing_profile = elisa_processing
lab_profile.add_panel(hiv_elisa_panel)

cd4_panel = RequisitionPanel('CD4', wb)
cd4_panel.processing_profile = cd4_processing
lab_profile.add_panel(cd4_panel)

site_labs.register('td_lab.maternalrequisition', lab_profile)
