from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel

sync_models = []

entry_models = [
    'td_maternal.maternaleligibility', 'td_maternal.maternaleligibilityloss', 'td_maternal.maternalconsent',
    'td_maternal.maternalvisit']

sync_models += entry_models

offstudy_models = ['td_maternal.maternaldeathreport', 'td_maternal.maternaloffstudy']

sync_models += offstudy_models

maternal_enrollment_models = [
    'td_maternal.antenatalenrollment', 'td_maternal.specimenconsent', 'td_maternal.antenatalenrollmenttwo',
    'td_maternal.maternallabourdel']

sync_models += maternal_enrollment_models

maternal_crfs = [
    'td_maternal.maternallocator', 'td_maternal.maternalultrasoundinitial', 'td_maternal.maternalobstericalhistory',
    'td_maternal.maternalmedicalhistory', 'td_maternal.maternaldemographics', 'td_maternal.maternallifetimearvhistory',
    'td_maternal.maternalarvpreg', 'td_maternal.maternalclinicalmeasurementsone', 'td_maternal.maternalrando',
    'td_maternal.rapidtestresult', 'td_maternal.maternaldiagnoses', 'td_maternal.maternalsubstanceusepriorpreg',
    'td_maternal.maternalhivinterimhx', 'td_maternal.maternalarv', 'td_maternal.maternalsubstanceuseduringpreg',
    'td_maternal.nvpdispensing', 'td_maternal.maternalpostpartumfu', 'td_maternal.maternalpostpartumdep',
    'td_maternal.maternalarvpost', 'td_maternal.maternalarvpostmed', 'td_maternal.maternalarvpostadh',
    'td_maternal.maternalinterimidcc', 'td_maternal.maternallifetimearvhistory', 'td_maternal.maternalinterimidcc',
    'td_maternal.maternalclinicalmeasurementstwo']

sync_models += maternal_crfs

infant_enrollment_models = ['td_infant.infantbirthdata']

sync_models += infant_enrollment_models

infant_crfs = [
    'td_infant.infantbirthexam', 'td_infant.infantbirthfeedingvaccine',
    'td_infant.infantbirtharv', 'td_infant.infantcongenitalanomalies',
    'td_infant.infantdeathreport', 'td_infant.infantfu', 'td_infant.infantfuphysical',
    'td_infant.infantfudx', 'td_infant.infantfudxitems', 'td_infant.infantfunewmed',
    'td_infant.InfantFuNewMedItems', 'td_infant.infantarvproph', 'td_infant.infantarvprophmod',
    'td_infant.infantfeeding', 'td_infant.infantfuimmunizations', 'td_infant.vaccinesreceived',
    'td_infant.vaccinesmissed', 'td_infant.solidfoodassessment', 'td_infant.infantvisit',
    'td_infant.infantbirth', 'td_infant.infantoffstudy', 'td_infant.infantvaccines',
    'td_infant.infantcns', 'td_infant.infantfacialdefect',
    'td_infant.infantcleftdisorder', 'td_infant.infantmouthupgi', 'td_infant.infantcardiodisorder',
    'td_infant.infantrespiratorydefect', 'td_infant.infantlowergi', 'td_infant.infantfemalegenital',
    'td_infant.infantrenal', 'td_infant.infantmusculoskeletal', 'td_infant.infantskin', 'td_infant.infanttrisomies',
    'td_infant.infantotherabnormalityitems', 'td_infant.infantmalegenital']

sync_models += infant_crfs

other_models = [
    'td_call_manager.call',
    'td_call_manager.log',
    'td_call_manager.logentry',
    'td_lab.panel',
    'td_lab.maternalrequisition',
    'td_lab.infantrequisition',
    'td_lab.receive',
    'td_lab.specimencollection',
    'td_lab.specimencollectionitem',
    'td_appointment.appointment',
    'td_registration.registeredsubject']

sync_models += other_models

site_sync_models.register(sync_models, SyncModel)
