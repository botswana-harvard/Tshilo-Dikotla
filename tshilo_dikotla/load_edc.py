import os
from unipath import Path
from django.contrib import admin

from edc_call_manager.caller_site import site_model_callers
from edc_data_manager.data_manager import data_manager
from td_list.models import RandomizationItem


def load_edc():

    f = open(os.path.join(
             Path(os.path.dirname(os.path.realpath(__file__))).ancestor(2).child('etc'), 'randomization.csv'))
    for index, line in enumerate(f.readlines()):
        if index == 0:
            continue
        seq, drug_assignment = line.split(',')
        RandomizationItem.objects.get_or_create(name=seq, field_name=drug_assignment)

    data_manager.prepare()
    site_model_callers.autodiscover()
    admin.autodiscover()
