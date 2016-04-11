LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_false'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'edc.core.crypto_fields.classes.cryptor': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'edc_lab.lab_clinic_api.managers.lab_manager': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'edc_lab.lab_clinic_api.classes.updater': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'edc_lab.lab_clinic_api.management.commands.update_labs': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'lis.exim.lab_import_dmis.classes.dmis': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'lis.exim.lab_import.classes.base_lock': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'lis.exim.lab_import_lis.classes.lis': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'lis.exim.lab_import.classes.base_import_history': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'edc_lab.lab_clinic_api.managers.lab_manager': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'edc_lab.lab_clinic_api.managers.result_manager': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'lis.core.lab_flag.classes.flag': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'edc_lab.lab_clinic_api.classes.dmis_result': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'lab_clinic_reference.classes.import_reference_range': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'lab_clinic_reference.classes.base_import': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'lab_receive.classes.receive_identifier': {
            'handlers': ['console', ],
            'level': 'WARNING',
        },
    }
}
