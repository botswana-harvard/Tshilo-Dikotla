from datetime import datetime, date

from edc_lab.lab_packing.models import DestinationTuple
from edc_lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc_configuration.base_app_configuration import BaseAppConfiguration
from edc_device import Device

from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

from .constants import MIN_AGE_OF_CONSENT

try:
    from config.labels import aliquot_label
except ImportError:
    aliquot_label = None

study_start_datetime = datetime(2016, 4, 1, 0, 0, 0)
study_end_datetime = datetime(2016, 12, 1, 0, 0, 0)


class AppConfiguration(BaseAppConfiguration):

    global_configuration = {
        'dashboard':
            {'show_not_required': True,
             'allow_additional_requisitions': False,
             'show_drop_down_requisitions': True},
        'appointment':
            {'allowed_iso_weekdays': ('12345', False),
             'use_same_weekday': True,
             'default_appt_type': 'clinic',
             'appointments_per_day_max': 20,
             'appointments_days_forward': 15},
        'protocol': {
            'start_datetime': study_start_datetime,
            'end_datetime': study_end_datetime},
    }

    study_variables_setup = {
        'protocol_number': 'BHP085',
        'protocol_code': '085',
        'protocol_title': 'BHP085',
        'research_title': 'Tshilo Dikotla',
        'study_start_datetime': study_start_datetime,
        'minimum_age_of_consent': MIN_AGE_OF_CONSENT,
        'maximum_age_of_consent': 50,
        'gender_of_consent': 'F',
        'subject_identifier_seed': '10000',
        'subject_identifier_prefix': '000',
        'subject_identifier_modulus': '7',
        'subject_type': 'subject',
        'machine_type': 'SERVER',
        'hostname_prefix': '0000',
        'device_id': Device().device_id}

    holidays_setup = {
        'New Year': date(2016, 1, 1),
        'New Year Holiday': date(2016, 1, 2),
        'Good Friday': date(2016, 3, 25),
        'Easter Monday': date(2016, 3, 28),
        'Labour Day': date(2016, 5, 1),
        'Labour Day Holiday': date(2016, 5, 2),
        'Ascension Day': date(2016, 5, 5),
        'Sir Seretse Khama Day': date(2016, 7, 1),
        'President\'s Day': date(2016, 7, 18),
        'President\'s Day Holiday': date(2016, 7, 19),
        'Independence Day': date(2016, 9, 30),
        'Botswana Day Holiday': date(2016, 10, 1),
        'Christmas Day': date(2016, 12, 25),
        'Boxing Day': date(2016, 12, 26)}

    consent_type_setup = [
        {'app_label': 'td_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': study_start_datetime,
         'end_datetime': datetime(2016, 12, 31, 23, 59),
         'version': '1'}
    ]

    study_site_setup = []

    lab_clinic_api_setup = {
        'panel': [PanelTuple('CD4', 'TEST', 'WB'),
                  PanelTuple('PBMC VL', 'TEST', 'WB'),
                  PanelTuple('Infant Glucose', 'TEST', 'WB'),
                  PanelTuple('Fasting Glucose', 'TEST', 'WB'),
                  PanelTuple('Glucose 1h', 'TEST', 'WB'),
                  PanelTuple('Glucose 2h', 'TEST', 'WB'),
                  PanelTuple('Infant Insulin', 'TEST', 'WB'),
                  PanelTuple('DNA PCR', 'TEST', 'WB'),
                  PanelTuple('PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB'),
                  PanelTuple('ELISA', 'TEST', 'WB'),],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                         AliquotTypeTuple('PBMC', 'PBMC', '31'),
                         AliquotTypeTuple('Serum', 'SERUM', '06')]}

    lab_setup = {'tshilo_dikotla': {
                 'destination': [DestinationTuple('BHHRL', 'Botswana-Harvard HIV Reference Laboratory',
                                                  'Gaborone', '3902671', 'bhhrl@bhp.org.bw')],
                 'panel': [PanelTuple('CD4', 'TEST', 'WB'),
                           PanelTuple('PBMC VL', 'TEST', 'WB'),
                           PanelTuple('Infant Glucose', 'TEST', 'WB'),
                           PanelTuple('Fasting Glucose', 'TEST', 'WB'),
                           PanelTuple('Glucose 1h', 'TEST', 'WB'),
                           PanelTuple('Glucose 2h', 'TEST', 'WB'),
                           PanelTuple('Infant Insulin', 'TEST', 'WB'),
                           PanelTuple('DNA PCR', 'TEST', 'WB'),
                           PanelTuple('PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB'),
                           PanelTuple('ELISA', 'TEST', 'WB'),
                           PanelTuple('Insulin', 'TEST', 'WB'),
                           PanelTuple('Infant PBMC PL', 'TEST', 'WB')],
                 'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                  AliquotTypeTuple('Plasma', 'PL', '32'),
                                  AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                                  AliquotTypeTuple('PBMC', 'PBMC', '31'),
                                  AliquotTypeTuple('Serum', 'SERUM', '06')],
                 'profile': [ProfileTuple('PBMC VL', 'WB'),
                             ProfileTuple('Glucose', 'WB'),
                             ProfileTuple('ELISA', 'WB'),
                             ProfileTuple('CD4', 'WB'),
                             ProfileTuple('PBMC Plasma (STORE ONLY)', 'WB'),
                             ProfileTuple('Infant Insulin', 'SERUM'),
                             ProfileTuple('Infant Glucose', 'WB'),
                             ProfileTuple('Infant PBMC PL', 'WB')],
                 'profile_item': [ProfileItemTuple('PBMC VL', 'PL', 1.0, 4),
                                  ProfileItemTuple('PBMC VL', 'PBMC', 0.5, 4),
                                  ProfileItemTuple('Glucose', 'PL', 1, 3),
                                  ProfileItemTuple('ELISA', 'PL', 1.0, 1),
                                  ProfileItemTuple('ELISA', 'BC', 0.5, 1),
                                  ProfileItemTuple('PBMC Plasma (STORE ONLY)', 'PL', 1, 4),
                                  ProfileItemTuple('PBMC Plasma (STORE ONLY)', 'PBMC', 1, 4),
                                  ProfileItemTuple('Infant Insulin', 'SERUM', 0.5, 1),
                                  ProfileItemTuple('Infant Glucose', 'PL', 0.5, 1),
                                  ProfileItemTuple('Infant PBMC PL', 'PL', 1.0, 2),
                                  ProfileItemTuple('Infant PBMC PL', 'PBMC', 1.0, 2)]}}
    labeling_setup = {
        'zpl_template': [
            aliquot_label or ZplTemplateTuple(
                'aliquot_label', (
                    ('^XA\n' +
                     ('^FO315,15^A0N,17,20^FD${protocol} Site ${site} ${clinician_initials}   '
                      '${aliquot_type} ${aliquot_count}${primary}^FS\n') +
                     '^FO320,34^BY1,3.0^BCN,50,N,N,N\n'
                     '^BY^FD${aliquot_identifier}^FS\n'
                     '^FO315,92^A0N,18,20^FD${aliquot_identifier}^FS\n'
                     '^FO315,109^A0N,16,20^FD${panel}^FS\n'
                     '^FO315,125^A0N,19,20^FD${subject_identifier} (${initials})^FS\n'
                     '^FO315,145^A0N,18,20^FDDOB: ${dob} ${gender}^FS\n'
                     '^FO315,165^A0N,18,20^FD${drawn_datetime}^FS\n'
                     '^XZ')), False),
            ZplTemplateTuple(
                'requisition_label', (
                    ('^XA\n' +
                     ('^FO315,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   '
                      '${aliquot_type} ${aliquot_count}${primary}^FS\n') +
                     '^FO315,34^BY1,3.0^BCN,50,N,N,N\n'
                     '^BY^FD${requisition_identifier}^FS\n'
                     '^FO315,92^A0N,20,20^FD${requisition_identifier} ${panel}^FS\n'
                     '^FO315,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                     '^FO315,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                     '^FO315,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                     '^XZ')), True)]
    }
#     labeling_setup = {
#         'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t',
#                                             'mpepu02', '192.168.1.230', True),
#                           LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t',
#                                             'kseamolo', '192.168.1.225', True)],
#         'client': [
#             ClientTuple(
#                 hostname='mpepu02',
#                 printer_name='Zebra_Technologies_ZTC_GK420t',
#                 cups_hostname='mpepu02',
#                 ip='192.168.1.230',
#                 aliases=None),
#             ClientTuple(
#                 hostname='kseamolo',
#                 printer_name='Zebra_Technologies_ZTC_GK420t',
#                 cups_hostname='kseamolo',
#                 ip='192.168.1.225',
#                 aliases=None)],
#         'zpl_template': [
#             aliquot_label or ZplTemplateTuple(
#                 'aliquot_label', (
#                     ('^XA\n' +
#                      ('^FO315,15^A0N,17,20^FD${protocol} Site ${site} ${clinician_initials}   '
#                       '${aliquot_type} ${aliquot_count}${primary}^FS\n') +
#                      '^FO320,34^BY1,3.0^BCN,50,N,N,N\n'
#                      '^BY^FD${aliquot_identifier}^FS\n'
#                      '^FO315,92^A0N,18,20^FD${aliquot_identifier}^FS\n'
#                      '^FO315,109^A0N,16,20^FD${panel}^FS\n'
#                      '^FO315,125^A0N,19,20^FD${subject_identifier} (${initials})^FS\n'
#                      '^FO315,145^A0N,18,20^FDDOB: ${dob} ${gender}^FS\n'
#                      '^FO315,165^A0N,18,20^FD${drawn_datetime}^FS\n'
#                      '^XZ')), False),
#             ZplTemplateTuple(
#                 'requisition_label', (
#                     ('^XA\n' +
#                      ('^FO310,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   '
#                       '${aliquot_type} ${aliquot_count}${primary}^FS\n') +
#                      '^FO310,34^BY1,3.0^BCN,50,N,N,N\n'
#                      '^BY^FD${requisition_identifier}^FS\n'
#                      '^FO310,92^A0N,20,20^FD${requisition_identifier} ${panel}^FS\n'
#                      '^FO310,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
#                      '^FO310,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
#                      '^FO310,152^A0N,25,20^FD${drawn_datetime}^FS\n'
#                      '^XZ')), True)]
#     }
