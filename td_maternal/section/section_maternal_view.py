from __future__ import print_function

from django.conf import settings
from django.contrib.auth.decorators import login_required

from edc_dashboard.section import BaseSectionView, site_sections

from ..models import MaternalEligibility
from ..search import MaternalSearchByWord


class MostRecentQuery(object):

    def __init__(self, model_cls, order_by=None, query_options=None, limit=None):
        self._model_cls = model_cls
        self._limit = limit or 50
        self._query_options = query_options or {}
        self._order_by = order_by or ('-modified')

    def get_model_cls(self):
        return self._model_cls

    def get_limit(self):
        return self._limit

    def get_query_options(self):
        return self._query_options

    def get_order_by(self):
        return self._order_by

    def query(self):
        qs = self.get_model_cls().objects.filter(
            **self.get_query_options())[0:self.get_limit()]

        qs_td_consent_version = [ml for ml in qs if ml.td_consent_version]
        qs_no_td_consent_version = [
            ml for ml in qs if not ml.td_consent_version]
        qs_td_consent_version = sorted(
            qs_td_consent_version,
            key=lambda eligibility: eligibility.td_consent_version.modified,
            reverse=True)

        qs_no_td_consent_version = sorted(
            qs_no_td_consent_version,
            key=lambda eligibility: eligibility.modified,
            reverse=True)

        qs = qs_td_consent_version + qs_no_td_consent_version

        return qs


class SectionMaternalView(BaseSectionView):
    section_name = 'maternal'
    section_display_name = 'Mothers'
    section_display_index = 10
    section_template = 'section_maternal.html'
    dashboard_url_name = 'subject_dashboard_url'
    add_model = MaternalEligibility
    search = {'word': MaternalSearchByWord}
    show_most_recent = True

    def _view(self, request, *args, **kwargs):
        """Wraps :func:`view` method to force login and treat this
        like a class based view.
        """
        @login_required
        def view(request, *args, **kwargs):
            self.context = {}
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            if self.search:
                self.searcher = self.search.get(
                    kwargs.get('search_name', 'word'))()
                self.searcher.search_form_data = request.POST or {
                    'search_term': kwargs.get('search_term')}
                if self.searcher.search_form(self.searcher.search_form_data).is_valid():
                    self.context.update({
                        'search_result': self._paginate(self.searcher.search_result, page),
                        'search_result_include_file': self.searcher.search_result_include_template})
                else:
                    if self.show_most_recent:
                        self.context.update({
                            'search_result': self._paginate(MostRecentQuery(
                                self.searcher.search_model).query(), page),
                            'search_result_include_file': self.searcher.search_result_include_template})
            self.context.update({
                'app_name': settings.APP_NAME,
                'installed_apps': settings.INSTALLED_APPS,
                'selected_section': self.section_name,
                'sections': self.section_list,
                'sections_names': [sec[0] for sec in self.section_list],
                'section_name': self.section_name,
                'protocol_lab_section': self.protocol_lab_section})
            try:
                self.context.update({
                    'add_model': self.add_model,
                    'add_model_opts': self.add_model._meta,
                    'add_model_name': self.add_model._meta.verbose_name})
            except AttributeError:
                pass
            self._contribute_to_context_wrapper(
                self.context, request, **kwargs)
            if self.search:
                self.searcher.contribute_to_context(self.context)
            return self.view(request, *args, **kwargs)
        return view(request, *args, **kwargs)


site_sections.register(SectionMaternalView)
