from django import template

from edc_base.utils import age

register = template.Library()


@register.simple_tag(takes_context=True)
def age_in_years(context, born):
    return age(born, context['reference_datetime']).years
