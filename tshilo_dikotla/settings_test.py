from .settings import *

MIGRATION_MODULES = {"tshilo_dikotla.apps.td_infant": "tshilo_dikotla.apps.td_infant.migrations_not_used_in_tests",
                     "tshilo_dikotla.apps.td_maternal": "tshilo_dikotla.apps.td_maternal.migrations_not_used_in_tests",
                     "edc_content_type_map": "edc_content_type_map.migrations_not_used_in_tests",
                     "edc_visit_schedule": "edc_visit_schedule.migrations_not_used_in_tests",
                     "edc_appointment": "edc_appointment.migrations_not_used_in_tests",
                     "edc_call_manager": "edc_call_manager.migrations_not_used_in_tests",
                     "edc_death_report": "edc_death_report.migrations_not_used_in_tests",
                     "edc_identifier": "edc_identifier.migrations_not_used_in_tests",
                     "edc_meta_data": "edc_meta_data.migrations_not_used_in_tests",
                     "edc_consent": "edc_consent.migrations_not_used_in_tests",
                     "edc_registration": "edc_registration.migrations_not_used_in_tests"}
