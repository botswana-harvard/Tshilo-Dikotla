from datetime import datetime, date
from edc_configuration.base_app_configuration import BaseAppConfiguration
from edc_device import Device
from edc_lab.lab_packing.models import DestinationTuple
from edc_lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

from .constants import MIN_AGE_OF_CONSENT


try:
    from config.labels import aliquot_label
except ImportError:
    aliquot_label = None

study_start_datetime = datetime(2016, 4, 1, 0, 0, 0)
study_end_datetime = datetime(2020, 12, 1, 0, 0, 0)


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
        'New Year': date(2017, 1, 1),
        'New Year Holiday': date(2017, 1, 2),
        'Good Friday': date(2017, 4, 14),
        'Easter Monday': date(2017, 4, 17),
        'Labour Day': date(2017, 5, 1),
        'Ascension Day': date(2017, 5, 25),
        'Sir Seretse Khama Day': date(2017, 7, 1),
        'President\'s Day': date(2017, 7, 17),
        'President\'s Day Holiday': date(2017, 7, 18),
        'Independence Day': date(2017, 9, 30),
        'Botswana Day Holiday': date(2017, 10, 1),
        'Botswana Day Holiday': date(2017, 10, 2),
        'Christmas Day': date(2017, 12, 25),
        'Boxing Day': date(2017, 12, 26)}

    consent_type_setup = [
        {'app_label': 'td_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': study_start_datetime,
         'end_datetime': datetime(2018, 12, 31, 23, 59),
         'version': '1'},
        {'app_label': 'td_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': datetime(2018, 1, 31, 23, 59),
         'end_datetime': datetime(2018, 12, 31, 23, 59),
         'version': '3'}
    ]

    study_site_setup = []

    lab_clinic_api_setup = {
        'panel': [PanelTuple('CD4', 'TEST', 'WB'),
                  PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('PBMC VL', 'TEST', 'WB'),
                  PanelTuple('Infant Glucose', 'TEST', 'WB'),
                  PanelTuple('Fasting Glucose', 'TEST', 'WB'),
                  PanelTuple('Glucose 1h', 'TEST', 'WB'),
                  PanelTuple('Glucose 2h', 'TEST', 'WB'),
                  PanelTuple('Infant Insulin', 'TEST', 'WB'),
                  PanelTuple('DNA PCR', 'TEST', 'WB'),
                  PanelTuple('PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB'),
                  PanelTuple('ELISA', 'TEST', 'WB'), ],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                         AliquotTypeTuple('PBMC', 'PBMC', '31'),
                         AliquotTypeTuple('Serum', 'SERUM', '06')]}

    lab_setup = {'tshilo_dikotla': {
                 'destination': [DestinationTuple('BHHRL', 'Botswana-Harvard HIV Reference Laboratory',
                                                  'Gaborone', '3902671', 'bhhrl@bhp.org.bw')],
                 'panel': [PanelTuple('CD4', 'TEST', 'WB'),
                           PanelTuple('Viral Load', 'TEST', 'WB'),
                           PanelTuple('PBMC VL', 'TEST', 'WB'),
                           PanelTuple('Infant Glucose', 'TEST', 'WB'),
                           PanelTuple('Fasting Glucose', 'TEST', 'WB'),
                           PanelTuple('Glucose 1h', 'TEST', 'WB'),
                           PanelTuple('Glucose 2h', 'TEST', 'WB'),
                           PanelTuple('Infant Insulin', 'TEST', 'WB'),
                           PanelTuple('DNA PCR', 'TEST', 'WB'),
                           PanelTuple(
                               'PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB'),
                           PanelTuple('ELISA', 'TEST', 'WB'),
                           PanelTuple('Insulin', 'TEST', 'WB'),
                           PanelTuple('Infant PBMC PL', 'TEST', 'WB'),
                           PanelTuple(
                               'Infant Serum (Store Only)', 'STORAGE', 'WB'),
                           PanelTuple('DBS (Store Only)', 'STORAGE', 'WB')],
                 'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                  AliquotTypeTuple('Plasma', 'PL', '32'),
                                  AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                                  AliquotTypeTuple('PBMC', 'PBMC', '31'),
                                  AliquotTypeTuple('Serum', 'SERUM', '06')],
                 'profile': [ProfileTuple('Viral Load', 'WB'),
                             ProfileTuple('PBMC VL', 'WB'),
                             ProfileTuple('Glucose', 'WB'),
                             ProfileTuple('ELISA', 'WB'),
                             ProfileTuple('CD4', 'WB'),
                             ProfileTuple('PBMC Plasma (STORE ONLY)', 'WB'),
                             ProfileTuple('Infant Glucose', 'WB'),
                             ProfileTuple('Infant PBMC PL', 'WB'),
                             ProfileTuple(
                                 'Infant Serum (Store Only)', 'SERUM'),
                             ProfileTuple('DBS (Store Only)', 'WB')],
                 'profile_item': [ProfileItemTuple('Viral Load', 'PL', 1.0, 3),
                                  ProfileItemTuple('Viral Load', 'BC', 0.5, 1),
                                  ProfileItemTuple('PBMC VL', 'PL', 1.0, 4),
                                  ProfileItemTuple('PBMC VL', 'PBMC', 0.5, 4),
                                  ProfileItemTuple('Glucose', 'PL', 1, 3),
                                  ProfileItemTuple('ELISA', 'PL', 1.0, 1),
                                  ProfileItemTuple('ELISA', 'BC', 0.5, 1),
                                  ProfileItemTuple(
                                      'PBMC Plasma (STORE ONLY)', 'PL', 1, 4),
                                  ProfileItemTuple(
                                      'PBMC Plasma (STORE ONLY)', 'PBMC', 1, 4),
                                  ProfileItemTuple(
                                      'Infant Glucose', 'PL', 0.5, 1),
                                  ProfileItemTuple(
                                      'Infant Serum (Store Only)', 'SERUM', 0.5, 1),
                                  ProfileItemTuple(
                                      'Infant PBMC PL', 'PL', 1.0, 2),
                                  ProfileItemTuple(
                                      'Infant PBMC PL', 'PBMC', 1.0, 7),
                                  ProfileItemTuple('DBS (Store Only)', 'WB', 0.5, 1)]}}
    labeling_setup = {
        'zpl_template': [
            aliquot_label or ZplTemplateTuple(
                'aliquot_label', (
                    ('^XA\n' +
                     ('~SD20^FO315,15^A0N,17,20^FD${protocol} Site ${site} ${clinician_initials}   '
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
