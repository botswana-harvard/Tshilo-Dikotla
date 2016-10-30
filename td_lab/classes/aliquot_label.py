from edc_label.actions import print_labels_action

from td_registration.models import RegisteredSubject


def print_aliquot_label(modeladmin, request, qs):
    """ Prints an aliquot label."""
    registered_subject = RegisteredSubject.objects.get(subject_identifier=qs[0].subject_identifier())
    extra_context = {
        'subject_identifier': registered_subject.subject_identifier,
        'gender': registered_subject.gender,
        'dob': registered_subject.dob,
        'initials': registered_subject.initials,
    }
    print_labels_action('aliquot', qs, request, extra_context)

print_aliquot_label.short_description = "LABEL: print aliquot label"
