from edc_registration.models import RegisteredSubject

from django.contrib import messages

from edc_label.label import Label


def print_aliquot_label(modeladmin, request, aliquots):
    """ Prints an aliquot label."""
    subject_identifier = aliquots[0].get_subject_identifier()
    registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifier)
    primary = ''
    if aliquots[0].aliquot_identifier[-2:] == '01':
        primary = "<"
    context = {}
    context.update({
            'aliquot_identifier': [al.aliquot_identifier for al in aliquots],})
    label_name = 'aliquot'
    labelling = Label(context, label_name)
    labelling.print_label(aliquots.count())
    messages.add_message(request, messages.SUCCESS, str(labelling.message))
print_aliquot_label.short_description = "LABEL: print aliquot label"
