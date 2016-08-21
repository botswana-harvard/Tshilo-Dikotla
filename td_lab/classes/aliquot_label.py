from edc_registration.models import RegisteredSubject

from django.contrib import messages

from edc_label.label import Label


def print_aliquot_label(model_name, request, aliquots):
    """ Prints an aliquot label."""
    context = {}
    label_name = 'aliquot'
    labelling = Label(context, label_name)
    labelling.print_label(aliquots.count())
    messages.add_message(request, messages.SUCCESS, str(labelling.message))
print_aliquot_label.short_description = "LABEL: print aliquot label"
