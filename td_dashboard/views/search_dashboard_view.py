from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from edc_base.view_mixins import EdcBaseViewMixin

from td_maternal.models import MaternalEligibility, MaternalConsent

from ..forms import MaternalEligibilityCrispyForm


class QuerysetWrapper:
    def __init__(self, qs):
        self.qs = qs or []
        self._object_list = []

    @property
    def object_list(self):
        if not self._object_list:
            for obj in self.qs:
                try:
                    maternal_consent = MaternalConsent.objects.get(maternal_eligibility_reference=obj.reference)
                    obj.maternal_consent_pks = [str(maternal_consent.pk)]
                    obj.subject_identifier = maternal_consent.subject_identifier
                except MultipleObjectsReturned:
                    maternal_consents = MaternalConsent.objects.filter(maternal_eligibility_reference=obj.reference)
                    obj.maternal_consent_pks = [
                        str(obj.pk) for obj in maternal_consents]
                    obj.subject_identifier = maternal_consents[0].subject_identifier
                except MaternalConsent.DoesNotExist:
                    obj.maternal_consent_pks = None
                    obj.subject_identifier = None
                if obj.subject_identifier:
                    obj.subject_label = obj.subject_identifier
                elif obj.is_eligible:
                    obj.subject_label = 'pending consent'
                elif not obj.is_eligible:
                    obj.subject_label = 'not eligible'
                self._object_list.append(obj)
        return self._object_list


class SearchDasboardView(EdcBaseViewMixin, TemplateView, FormView):
    form_class = MaternalEligibilityCrispyForm
    template_name = 'td_dashboard/search_dashboard.html'
    paginate_by = 10

    def __init__(self, **kwargs):
        self.maternal_eligibility = None
        super(SearchDasboardView, self).__init__(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchDasboardView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            subject_identifier = form.cleaned_data['subject_identifier']
            try:
                qs = [MaternalEligibility.objects.get(
                    subject_identifier__icontains=subject_identifier)]
            except MaternalEligibility.DoesNotExist:
                qs = None
                form.add_error(
                    'subject_identifier',
                    'Maternal eligibility not found for {}.'.format(subject_identifier))
            except MultipleObjectsReturned:
                qs = MaternalEligibility.objects.filter(
                    subject_identifier__icontains=subject_identifier).order_by('subject_identifier', '-created')
            context = self.get_context_data()
            context.update(
                form=form,
                results=self.paginate(QuerysetWrapper(qs).object_list))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SearchDasboardView, self).get_context_data(**kwargs)
        qs = MaternalEligibility.objects.all().order_by('subject_identifier', '-created')
        results = QuerysetWrapper(qs).object_list
        context.update(
            site_header=admin.site.site_header,
            results=self.paginate(results))
        return context

    def paginate(self, qs):
        paginator = Paginator(qs, self.paginate_by)
        try:
            page = paginator.page(self.kwargs.get('page', 1))
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page
