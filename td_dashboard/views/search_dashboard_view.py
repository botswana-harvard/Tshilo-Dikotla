from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView, FormView
from ..forms import MaternalEligibilityCrispyForm
from td_maternal.models.maternal_eligibility import MaternalEligibility
from td_infant.models.infant_birth import InfantBirth

from edc_base.view_mixins import EdcBaseViewMixin


class SearchDasboardView(EdcBaseViewMixin, TemplateView, FormView):
    form_class = MaternalEligibilityCrispyForm
    template_name = 'td_dashboard/search_dashboard2.html'

    def __init__(self, **kwargs):
        self.maternal_eligibility = None
        self.infant = None
        super(SearchDasboardView, self).__init__(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            subject_identifier = form.cleaned_data['subject_identifier']
            try:
                self.maternal_eligibility = MaternalEligibility.objects.get(
                    registered_subject__subject_identifier=subject_identifier)
                subject_identifier_infant = subject_identifier + '-10'
                try:
                    self.infant = InfantBirth.objects.get(
                        registered_subject__subject_identifier=subject_identifier_infant)
                except InfantBirth.DoesNotExist:
                    pass
            except MaternalEligibility.DoesNotExist:
                form.add_error('subject_identifier',
                               'Maternal eligibility not found. Please search again or add a new maternal eligibility.')
            context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SearchDasboardView, self).get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            site_header=admin.site.site_header,
            maternal_eligibilities=self.maternal_eligibilities
        )
        context.update({
            'infant': self.infant})
        return context

    @property
    def maternal_eligibilities(self):
        if self.maternal_eligibility is None:
            return MaternalEligibility.objects.all().order_by('-created')[:20]
        else:
            return [self.maternal_eligibility]
