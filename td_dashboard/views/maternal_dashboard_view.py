from collections import OrderedDict
from datetime import datetime

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.utils import convert_from_camel, get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import DashboardMixin
from edc_registration.models import RegisteredSubject

from td.constants import INFANT
from td_infant.models.infant_birth import InfantBirth
from td_maternal.maternal_hiv_status import MaternalHivStatus
from td_maternal.models import (
    AntenatalEnrollment, MaternalConsent, MaternalLabDel, MaternalLocator,
    MaternalRando, MaternalVisit)
from td_maternal.pregnancy import Pregnancy


class MaternalDashboardView(DashboardMixin, EdcBaseViewMixin, TemplateView):

    dashboard_url_name = 'subject_dashboard_url'
    add_visit_url_name = MaternalVisit().admin_url_name
    template_name = 'td_dashboard/subject_dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MaternalDashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MaternalDashboardView, self).get_context_data(**kwargs)
        reference_datetime = get_utcnow()
        try:
            maternal_rando = MaternalRando.objects.get(maternal_visit__subject_identifier=self.subject_identifier)
        except MaternalRando.DoesNotExist:
            maternal_rando = None
        try:
            maternal_consent = MaternalConsent.objects.get(subject_identifier=self.subject_identifier)
        except MaternalConsent.DoesNotExist:
            maternal_consent = None
        except MultipleObjectsReturned:
            maternal_consent = MaternalConsent.objects.filter(
                subject_identifier=self.subject_identifier).order_by('-version').first()
        try:
            maternal_lab_del = MaternalLabDel.objects.get(subject_identifier=self.subject_identifier)
        except MaternalLabDel.DoesNotExist:
            maternal_lab_del = None
        try:
            maternal_locator = MaternalLocator.objects.get(subject_identifier=self.subject_identifier)
        except MaternalLocator.DoesNotExist:
            maternal_locator = None
        maternal_hiv_status = MaternalHivStatus(
            subject_identifier=self.subject_identifier,
            reference_datetime=reference_datetime)
        pregnancy = Pregnancy(
            self.subject_identifier,
            reference_datetime=reference_datetime)
        context.update(
            add_visit_url_name=self.add_visit_url_name,
            maternal_rando=maternal_rando,
            maternal_consent=maternal_consent,
            maternal_hiv_status=maternal_hiv_status,
            pregnancy=pregnancy,
            maternal_lab_del=maternal_lab_del,
            maternal_locator=maternal_locator,
            enrollment_objects=self.enrollment_objects,
            reference_datetime=get_utcnow(),
        )
        return context

    @property
    def enrollment_objects(self):
        """ """
        enrollment_objects = []
        enrollments_models = [
            'td_maternal.specimenconsent', 'td_maternal.antenatalenrollment',
            'td_maternal.antenatalenrollmenttwo', 'td_maternal.maternallabdel']
        for model in enrollments_models:
            model = django_apps.get_model(*model.split('.'))
            try:
                enrollment_objects.append(model.objects.get(subject_identifier=self.subject_identifier))
            except model.DoesNotExist:
                enrollment_objects.append(model())
        return enrollment_objects

    @property
    def antenatal_enrollment_status(self):
        """Not used"""
        antenatal_enrollment_status = 'ERROR'
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(subject_identifier=self.subject_identifier)
            if antenatal_enrollment:
                if antenatal_enrollment.ga_pending:
                    antenatal_enrollment_status = 'Pending ultrasound'
                elif antenatal_enrollment.is_eligible:
                    antenatal_enrollment_status = 'Passed'
                elif not antenatal_enrollment.is_eligible:
                    antenatal_enrollment_status = 'Failed'
        except AntenatalEnrollment.DoesNotExist:
            antenatal_enrollment_status = 'Not filled'
        return antenatal_enrollment_status

    @property
    def currently_pregnant(self):
        """Not used"""
        if not self.maternal_delivery:
            return True
        return None

    @property
    def get_registered_infant_identifier(self):
        """Not used"""
        """Returns an infant identifier associated with the maternal identifier"""
        infants = OrderedDict()
        infant_registered_subject = None
        try:
            infant_registered_subject = RegisteredSubject.objects.get(
                subject_type=INFANT, relative_identifier__iexact=self.subject_identifier)
            try:
                infant_birth = InfantBirth.objects.get(registered_subject__exact=infant_registered_subject)
                dct = infant_birth.__dict__
                dct['dashboard_model'] = convert_from_camel(infant_birth._meta.object_name)
                dct['dashboard_id'] = convert_from_camel(str(infant_birth.pk))
                dct['dashboard_type'] = INFANT
                infants[infant_registered_subject.subject_identifier] = dct
            except InfantBirth.DoesNotExist:
                dct = {'subject_identifier': infant_registered_subject.subject_identifier}
                dct['dashboard_model'] = 'registered_subject'
                dct['dashboard_id'] = str(infant_registered_subject.pk)
                dct['dashboard_type'] = INFANT
                infants[infant_registered_subject.subject_identifier] = dct
        except RegisteredSubject.DoesNotExist:
            pass
        return infants
