from datetime import date, datetime

from edc_registration.models import RegisteredSubject

from lis.labeling.classes import ModelLabel
from lis.labeling.models import ZplTemplate


class RequisitionLabel(ModelLabel):

    def __init__(self):
        super(RequisitionLabel, self).__init__()
        self.zpl_template = ZplTemplate.objects.get(name='requisition_label')

    def test(self, client_addr, label_printer=None):
        """Passes a test label the printer.

        Accepts arg client_addr (hostname or ip)."""
        custom = {}
        custom.update({
            'requisition_identifier': 'ABCD1234',
            'aliquot_count': 1,
            'primary': '<',
            'panel': 'Research Blood Draw',
            'barcode_value': "ABCD1234",
            'protocol': 'BHP999',
            'site': 'SS',
            'clinician_initials': 'CC',
            'drawn_datetime': datetime.today().strftime('%Y-%m-%d %H:%M'),
            'subject_identifier': '999-990000-01',
            'gender': 'M',
            'dob': date.today(),
            'initials': 'erik',
            'aliquot_type': 'WB'})
        self.label_context.update(**custom)
        return super(RequisitionLabel, self).test(client_addr=client_addr, label_printer=label_printer)

    def refresh_label_context(self):
        requisition = self.model_instance
        subject_identifier = requisition.get_subject_identifier()
        registered_subject = RegisteredSubject.objects.get(
            subject_identifier=subject_identifier)
        primary = '<'
        custom = {}
        custom.update({
            'aliquot_count': 1,
            'aliquot_type': requisition.aliquot_type.alpha_code.upper(),
            'barcode_value': requisition.requisition_identifier,
            'clinician_initials': requisition.user_created[0:2].upper(),
            'dob': registered_subject.dob,
            'drawn_datetime': requisition.drawn_datetime,
            'gender': registered_subject.gender,
            'initials': registered_subject.initials,
            'panel': requisition.panel.name,
            'primary': primary,
            'protocol': subject_identifier[0:3],
            'requisition_identifier': requisition.requisition_identifier,
            'site': subject_identifier[4:6],
            'subject_identifier': subject_identifier,
        })
        self.label_context.update(**custom)

    def print_label_for_requisition(self, request, requisition):
        """ Prints a requisition label."""
        if requisition.requisition_identifier:
            self.print_label(request, requisition, 1)
