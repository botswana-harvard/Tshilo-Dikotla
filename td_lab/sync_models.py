from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel

sync_models = [
    'td_lab.panel',
    'td_lab.maternalrequisition',
    'td_lab.infantrequisition',
    'td_lab.receive',
    'td_lab.specimencollection',
    'td_lab.specimencollectionitem']

site_sync_models.register(sync_models, SyncModel)
