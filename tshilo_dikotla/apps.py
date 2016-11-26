import os
import pytz

from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR
from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings

from edc_appointment.apps import AppConfig as EdcAppointmentAppConfigParent
from edc_appointment.facility import Facility
from edc_base.apps import AppConfig as EdcBaseAppConfigParent
from edc_consent.apps import AppConfig as EdcConsentAppConfigParent
from edc_consent.consent_config import ConsentConfig
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_device.apps import AppConfig as EdcDeviceAppConfigParent
from edc_identifier.apps import AppConfig as EdcIdentifierAppConfigParent
from edc_lab.apps import AppConfig as EdcLabAppConfig
from edc_label.apps import AppConfig as EdcLabelConfigParent
from edc_metadata.apps import AppConfig as EdcMetadataAppConfigParent
from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent
from edc_sync.apps import AppConfig as EdcSyncAppConfigParent
from edc_sync.constants import SERVER
from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
from edc_timepoint.timepoint import Timepoint
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT


class AppConfig(DjangoAppConfig):
    name = 'tshilo_dikotla'
    verbose_name = 'Tshilo Dikotla'


class EdcDeviceAppConfig(EdcDeviceAppConfigParent):
    role = SERVER
    device_id = '99'
    server_id_list = [99]
    middleman_id_list = []


class EdcProtocolAppConfig(EdcProtocolAppConfigParent):
    protocol = 'BHP085'
    protocol_number = '085'
    protocol_name = 'Tshilo Dikotla'
    protocol_title = ''
    study_open_datetime = datetime(2016, 4, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
    study_end_datetime = datetime(2018, 12, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
    subject_types = {'maternal': 'maternal', 'infant': 'infant'}
    enrollment_caps = {'td_maternal.antenatalenrollment': ('maternal', -1),
                       'td_infant.infant_birth': ('infant', -1)}


class EdcBaseAppConfig(EdcBaseAppConfigParent):
    institution = 'Botswana Harvard AIDS Institute Partnership'
    project_name = 'Tshilo Dikotla'


class EdcConsentAppConfig(EdcConsentAppConfigParent):
    consent_configs = [
        ConsentConfig(
            'td_maternal.maternalconsent',
            start=datetime(2016, 5, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC')),
            end=datetime(2017, 10, 30, 0, 0, 0, tzinfo=pytz.timezone('UTC')),
            version='1',
            age_is_adult=18,
            age_max=64,
            gender=['F']),
    ]


class EdcAppointmentAppConfig(EdcAppointmentAppConfigParent):
    default_appt_type = 'clinic'
    facilities = {
        'clinic': Facility(name='clinic', days=[MO, TU, WE, TH, FR], slots=[10, 10, 10, 10, 10])}


class EdcTimepointAppConfig(EdcTimepointAppConfigParent):
    timepoints = [
        Timepoint(
            model='td.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
        Timepoint(
            model='td.historicalappointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
        Timepoint(
            model='edc_appointment.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
        Timepoint(
            model='edc_appointment.historicalappointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        )
    ]


class EdcLabelAppConfig(EdcLabelConfigParent):
    default_cups_server_ip = '10.113.201.114'
    default_printer_label = 'leslie_testing'
    default_template_file = os.path.join(settings.STATIC_ROOT, 'tshilo_dikotla', 'label_templates', 'aliquot.lbl')
    default_label_identifier_name = ''


class EdcSyncAppConfig(EdcSyncAppConfigParent):
    edc_sync_files_using = True


class EdcVisitTrackingAppConfig(EdcVisitTrackingAppConfigParent):
    visit_models = {'td_maternal': ('maternal_visit', 'td_maternal.maternalvisit'),
                    'td_infant': ('infant_visit', 'td_infant.infantvisit')}


class EdcIdentifierAppConfig(EdcIdentifierAppConfigParent):
    identifier_prefix = '085'


class EdcMetadataAppConfig(EdcMetadataAppConfigParent):
    app_label = 'td_maternal'
    crf_model_name = 'crfmetadata'
    requisition_model_name = 'requisitionmetadata'

    reason_field = {'td_maternal.maternalvisit': 'reason', 'td_infant.infantvisit': 'reason'}
    create_on_reasons = [SCHEDULED, UNSCHEDULED]
    delete_on_reasons = [LOST_VISIT, FAILED_ELIGIBILITY]


class EdcLabAppConfig(EdcLabAppConfig):
    app_label = 'td_lab'
    requisition = 'td_lab.maternalrequisition'
