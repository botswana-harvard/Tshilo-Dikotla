from django.contrib import admin
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import TemplateView, FormView

from td_maternal.models.maternal_eligibility import MaternalEligibility

from ..forms import MaternalEligibilityCrispyForm

from edc_base.view_mixins import EdcBaseViewMixin
from td_maternal.models.maternal_consent import MaternalConsent
from django.core.exceptions import MultipleObjectsReturned


class SearchDasboardView(EdcBaseViewMixin, TemplateView, FormView):
    form_class = MaternalEligibilityCrispyForm
    template_name = 'td_dashboard/search_dashboard.html'
    paginate_by = 10

    def __init__(self, **kwargs):
        self.maternal_eligibility = None
        self.infant = None
        super(SearchDasboardView, self).__init__(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            results = None
            try:
                results = [MaternalEligibility.objects.get(
                    maternal_consent__subject_identifier=form.cleaned_data['subject_identifier'])]
            except MaternalEligibility.DoesNotExist:
                results = None
                form.add_error(
                    'subject_identifier',
                    'Maternal eligibility not found for {}.'.format(form.cleaned_data['subject_identifier']))
            context = self.get_context_data(
                form=form,
                results=results)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SearchDasboardView, self).get_context_data(**kwargs)
        results = MaternalEligibility.objects.all().order_by('-created')
        for obj in results:
            try:
                maternal_consent = MaternalConsent.objects.get(maternal_eligibility_reference=obj.reference_pk)
                obj.subject_identifier = maternal_consent.subject_identifier
            except MaternalConsent.DoesNotExist:
                obj.subject_identifier = None
            except MultipleObjectsReturned:
                maternal_consent = MaternalConsent.objects.filter(maternal_eligibility_reference=obj.reference_pk)[0]
                obj.subject_identifier = maternal_consent.subject_identifier
        results_paginator = Paginator(results, self.paginate_by)
        try:
            results = results_paginator.page(self.kwargs.get('page', 1))
        except EmptyPage:
            results = results_paginator.page(results_paginator.num_pages)
        context.update(
            site_header=admin.site.site_header,
            results=results)
        context.update({
            'infant': self.infant})
        return context
