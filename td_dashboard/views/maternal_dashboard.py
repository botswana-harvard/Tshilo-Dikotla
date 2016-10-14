from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from ..forms import MaternalEligibilityCrispyForm
from td_maternal.models.maternal_eligibility import MaternalEligibility


class MaternalDasboard(TemplateView):

    template_name = 'td_dashboard/maternal_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            site_header=admin.site.site_header,
            form=MaternalEligibilityCrispyForm(),
            maternal_eligibilities=self.maternal_eligibilities
        )
        return context

    @property
    def maternal_eligibilities(self):
        return MaternalEligibility.objects.all()
