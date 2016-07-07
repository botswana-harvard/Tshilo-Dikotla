import os
from unipath import Path
from django.contrib import admin

from edc_base.utils import edc_base_startup
from edc_call_manager.caller_site import site_model_callers
from edc_dashboard.section import site_sections
from edc_data_manager.data_manager import data_manager
from edc_lab.lab_profile.classes import site_lab_profiles
from edc_rule_groups.classes import site_rule_groups
from edc_visit_schedule.classes import site_visit_schedules

from tshilo_dikotla.app_configuration import AppConfiguration
from td_list.models import RandomizationItem


def load_edc():

    f = open(os.path.join(
             Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1).child('etc'), 'randomization.csv'))
    for index, line in enumerate(f.readlines()):
        if index == 0:
            continue
        seq, drug_assignment = line.split(',')
        RandomizationItem.objects.get_or_create(name=seq, field_name=drug_assignment)

    edc_base_startup()
    site_lab_profiles.autodiscover()
    AppConfiguration(lab_profiles=site_lab_profiles).prepare()
    site_visit_schedules.autodiscover()
    site_visit_schedules.build_all()
    site_rule_groups.autodiscover()
    data_manager.prepare()
    site_sections.autodiscover()
    site_sections.update_section_lists()
    site_model_callers.autodiscover()
    admin.autodiscover()


