from edc_lab.aliquot.aliquot_type import AliquotType
from edc_lab.aliquot.processing_profile import ProcessingProfile
from edc_lab.lab_profile import LabProfile
from edc_lab.requisition.requisition_panel import RequisitionPanel
from edc_lab.site_lab_profiles import site_lab_profiles

lab_profile = LabProfile('clinic_lab')

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

# infant birth profiles
infant_birth_insulin_processing = ProcessingProfile('Infant Insulin', wb)
infant_birth_insulin_processing.add_process(serum, 1)
lab_profile.add_processing_profile(infant_birth_insulin_processing)

infant_birth_pbmc_pl_processing = ProcessingProfile('Infant PBMC PL', wb)
infant_birth_pbmc_pl_processing.add_process(pl, 2)
infant_birth_pbmc_pl_processing.add_process(bc, 2)
lab_profile.add_processing_profile(infant_birth_pbmc_pl_processing)

infant_glucose_processing = ProcessingProfile('Infant Glucose', wb)
infant_glucose_processing.add_process(pl, 1)
lab_profile.add_processing_profile(infant_glucose_processing)

# infant birth requisitions
infant_birth_pbmc_pl_panel = RequisitionPanel('Infant PBMC PL', wb)  # link this to the visit_schedule
infant_birth_pbmc_pl_panel.processing_profile = infant_birth_pbmc_pl_processing
lab_profile.add_panel(infant_birth_pbmc_pl_panel)

infant_glucose_panel = RequisitionPanel('Infant Glucose', wb)
infant_glucose_panel.processing_profile = infant_glucose_processing
lab_profile.add_panel(infant_glucose_panel)

infant_birth_insulin_panel = RequisitionPanel('Infant Insulin', wb)
infant_birth_insulin_panel.processing_profile = infant_birth_insulin_processing
lab_profile.add_panel(infant_birth_insulin_panel)

# infant postpartum 1 profiles
infant_pp1_insulin_processing = ProcessingProfile('Infant Insulin 1M', wb)
infant_pp1_insulin_processing.add_process(serum, 2)
lab_profile.add_processing_profile(infant_pp1_insulin_processing)

# PBMC/ PL and PCR for HEU infants
infant_pp1_heu_pbmc_pl_processing = ProcessingProfile('Infant HIV PCR PBMC PL', wb)
infant_pp1_heu_pbmc_pl_processing.add_process(pl, 3)
infant_pp1_heu_pbmc_pl_processing.add_process(bc, 2)
lab_profile.add_processing_profile(infant_pp1_heu_pbmc_pl_processing)

# PBMC/ PL for HUU infants
infant_pp1_huu_pbmc_pl_processing = ProcessingProfile('Infant PBMC PL 1M', wb)
infant_pp1_huu_pbmc_pl_processing.add_process(pl, 3)
infant_pp1_huu_pbmc_pl_processing.add_process(bc, 2)
lab_profile.add_processing_profile(infant_pp1_huu_pbmc_pl_processing)

# infant postpartum 18 profiles
infant_pp18_heu_insulin_processing = ProcessingProfile('Infant Insulin HIV Elisa', wb)
infant_pp18_heu_insulin_processing.add_process(serum, 3)
lab_profile.add_processing_profile(infant_pp18_heu_insulin_processing)

infant_pp18_huu_insulin_processing = ProcessingProfile('Infant Insulin 18M', wb)
infant_pp18_huu_insulin_processing.add_process(serum, 2)
lab_profile.add_processing_profile(infant_pp18_huu_insulin_processing)

# PBMC/ PL and PCR for HEU infants
infant_pp18_pbmc_pl_processing = ProcessingProfile('Infant PBMC PL 18M', wb)
infant_pp18_pbmc_pl_processing.add_process(pl, 2)
infant_pp18_pbmc_pl_processing.add_process(bc, 2)
lab_profile.add_processing_profile(infant_pp18_pbmc_pl_processing)

infant_heu_heel_stick_processing = ProcessingProfile('Infant Heelstick', wb)
lab_profile.add_processing_profile(infant_heu_heel_stick_processing)

# infant postpartum 36 profiles
infant_pp36_insulin_processing = ProcessingProfile('Infant Insulin 36M', wb)
infant_pp36_insulin_processing.add_process(serum, 3)
lab_profile.add_processing_profile(infant_pp36_insulin_processing)

# PBMC/ PL and PCR for HEU infants
infant_pp36_pbmc_pl_processing = ProcessingProfile('Infant PBMC PL 36M', wb)
infant_pp36_pbmc_pl_processing.add_process(pl, 4)
infant_pp36_pbmc_pl_processing.add_process(bc, 4)
lab_profile.add_processing_profile(infant_pp36_pbmc_pl_processing)

# infant post partum 1 requisitions
infant_pp1_heu_pbmc_pl_panel = RequisitionPanel('Infant HIV PCR PBMC PL', wb)  # link this to the visit_schedule
infant_pp1_heu_pbmc_pl_panel.processing_profile = infant_pp1_heu_pbmc_pl_processing
lab_profile.add_panel(infant_pp1_heu_pbmc_pl_panel)

infant_pp1_huu_pbmc_pl_panel = RequisitionPanel('Infant PBMC PL 1M', wb)  # link this to the visit_schedule
infant_pp1_huu_pbmc_pl_panel.processing_profile = infant_pp1_huu_pbmc_pl_processing
lab_profile.add_panel(infant_pp1_huu_pbmc_pl_panel)

infant_pp1_insulin_panel = RequisitionPanel('Infant Insulin 1M', wb)
infant_pp1_insulin_panel.processing_profile = infant_pp1_insulin_processing
lab_profile.add_panel(infant_pp1_insulin_panel)

infant_heelstick_panel = RequisitionPanel('Infant Heelstick', wb)
infant_heelstick_panel.processing_profile = infant_heu_heel_stick_processing
lab_profile.add_panel(infant_heelstick_panel)

# infant post partum 18 requisitions
infant_pp18_huu_pbmc_pl_panel = RequisitionPanel('Infant PBMC PL 18M', wb)  # link this to the visit_schedule
infant_pp18_huu_pbmc_pl_panel.processing_profile = infant_pp18_pbmc_pl_processing
lab_profile.add_panel(infant_pp18_huu_pbmc_pl_panel)

infant_pp18_heu_insulin_panel = RequisitionPanel('Infant Insulin HIV Elisa', wb)
infant_pp18_heu_insulin_panel.processing_profile = infant_pp18_heu_insulin_processing
lab_profile.add_panel(infant_pp18_heu_insulin_panel)

infant_pp18_huu_insulin_panel = RequisitionPanel('Infant Insulin 18M', wb)
infant_pp18_huu_insulin_panel.processing_profile = infant_pp18_huu_insulin_processing
lab_profile.add_panel(infant_pp18_huu_insulin_panel)

# infant post partum 36 requisitions
infant_pp36_pbmc_pl_panel = RequisitionPanel('Infant PBMC PL 36M', wb)  # link this to the visit_schedule
infant_pp36_pbmc_pl_panel.processing_profile = infant_pp36_pbmc_pl_processing
lab_profile.add_panel(infant_pp36_pbmc_pl_panel)

infant_pp36_insulin_panel = RequisitionPanel('Infant Insulin 36M', wb)
infant_pp36_insulin_panel.processing_profile = infant_pp36_insulin_processing
lab_profile.add_panel(infant_pp36_insulin_panel)

site_lab_profiles.register('td_infant.infantrequisition', lab_profile)
