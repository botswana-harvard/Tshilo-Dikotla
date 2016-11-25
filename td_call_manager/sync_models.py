from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel

sync_models = [
    'td_call_manager.call',
    'td_call_manager.log',
    'td_call_manager.logentry']

site_sync_models.register(sync_models, SyncModel)
