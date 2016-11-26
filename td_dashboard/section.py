from collections import namedtuple

from edc_dashboard.section import BaseSectionView, site_sections

ModelMeta = namedtuple('ModelMeta', 'app_label model_name')


class SectionAdministrationView(BaseSectionView):
    section_name = 'administration'
    section_display_name = 'Administration'
    section_display_index = 140
    section_template = 'tshilo_dikotla_section_admin.html'

    def contribute_to_context(self, context, request, *args, **kwargs):
        context.update({
            'maternal_meta': ModelMeta('td_maternal', 'maternal_eligibility'),
            'aliquot_type_meta': ModelMeta('td_lab', 'aliquot_type'),
            'aliquot_meta': ModelMeta('td_lab', 'aliquot'),
        })

site_sections.register(SectionAdministrationView, replaces='administration')
