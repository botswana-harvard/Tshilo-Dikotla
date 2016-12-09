from model_mommy import mommy

from django.apps import apps as django_apps

from td.models import Appointment


class AddVisitMixin:

    def add_visit(self, model_label, code, reason=None):
        """Adds (or gets) and returns a visit for give model and code."""
        reason = reason or 'scheduled'
        model = django_apps.get_model(*model_label.split('.'))
        appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code=code)
        try:
            visit = self.get_visit(model_label, code)
        except model.DoesNotExist:
            visit = mommy.make_recipe(
                model_label,
                appointment=appointment, reason=reason)
        return visit

    def add_visits(self, model_label, *codes):
        """Adds a sequence of visits for the codes provided.

        If a infant visit already exists, it will just pass."""
        for code in codes:
            self.add_visit(model_label, code)

    def get_visit(self, model_label, code):
        """Returns a visit instance if it exists."""
        model = django_apps.get_model(*model_label.split('.'))
        return model.objects.get(
            appointment__subject_identifier=self.subject_identifier, visit_code=code)
