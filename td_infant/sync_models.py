from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel

sync_models = [
    'td_infant.Infantfunewmeditems',
    'td_infant.infantarvproph',
    'td_infant.infantarvprophmod',
    'td_infant.infantbirth',
    'td_infant.infantbirtharv',
    'td_infant.infantbirthdata',
    'td_infant.infantbirthexam',
    'td_infant.infantbirthfeedingvaccine',
    'td_infant.infantcardiodisorder',
    'td_infant.infantcleftdisorder',
    'td_infant.infantcns',
    'td_infant.infantcongenitalanomalies',
    'td_infant.infantdeathreport',
    'td_infant.infantfacialdefect',
    'td_infant.infantfeeding',
    'td_infant.infantfemalegenital',
    'td_infant.infantfu',
    'td_infant.infantfudx',
    'td_infant.infantfudxitems',
    'td_infant.infantfuimmunizations',
    'td_infant.infantfunewmed',
    'td_infant.infantfuphysical',
    'td_infant.infantlowergi',
    'td_infant.infantmalegenital'
    'td_infant.infantmouthupgi',
    'td_infant.infantmusculoskeletal',
    'td_infant.infantoffstudy',
    'td_infant.infantotherabnormalityitems',
    'td_infant.infantrenal',
    'td_infant.infantrespiratorydefect',
    'td_infant.infantskin',
    'td_infant.infanttrisomies',
    'td_infant.infantvaccines',
    'td_infant.infantvisit',
    'td_infant.solidfoodassessment',
    'td_infant.vaccinesmissed',
    'td_infant.vaccinesreceived',
]

site_sync_models.register(sync_models, SyncModel)
