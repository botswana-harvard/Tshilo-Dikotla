from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel

sync_models = [
    'td_maternal.antenatalenrollment',
    'td_maternal.antenatalenrollmenttwo',
    'td_maternal.maternalarv',
    'td_maternal.maternalarvpost',
    'td_maternal.maternalarvpostadh',
    'td_maternal.maternalarvpostmed',
    'td_maternal.maternalarvpreg',
    'td_maternal.maternalclinicalmeasurementsone',
    'td_maternal.maternalclinicalmeasurementstwo'
    'td_maternal.maternalconsent',
    'td_maternal.maternaldeathreport',
    'td_maternal.maternaldemographics',
    'td_maternal.maternaldiagnoses',
    'td_maternal.maternaleligibility',
    'td_maternal.maternaleligibilityloss',
    'td_maternal.maternalhivinterimhx',
    'td_maternal.maternalinterimidcc',
    'td_maternal.maternallabourdel'
    'td_maternal.maternallifetimearvhistory',
    'td_maternal.maternallocator',
    'td_maternal.maternalmedicalhistory',
    'td_maternal.maternalobstericalhistory',
    'td_maternal.maternaloffstudy',
    'td_maternal.maternalpostpartumdep',
    'td_maternal.maternalpostpartumfu',
    'td_maternal.maternalrando',
    'td_maternal.maternalsubstanceuseduringpreg',
    'td_maternal.maternalsubstanceusepriorpreg',
    'td_maternal.maternalultrasoundinitial',
    'td_maternal.maternalvisit',
    'td_maternal.nvpdispensing',
    'td_maternal.rapidtestresult',
    'td_maternal.specimenconsent',
]

site_sync_models.register(sync_models, SyncModel)
