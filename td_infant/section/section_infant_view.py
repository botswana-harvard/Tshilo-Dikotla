from edc_dashboard.section import BaseSectionView, site_sections

from tshilo_dikotla.constants import INFANT

from ..search import InfantSearchByWord


class SectionInfantView(BaseSectionView):
    section_name = INFANT
    section_display_name = 'Infants'
    section_display_index = 30
    section_template = 'section_infant.html'
    dashboard_url_name = 'subject_dashboard_url'
    search = {'word': InfantSearchByWord}
    show_most_recent = True

site_sections.register(SectionInfantView)
