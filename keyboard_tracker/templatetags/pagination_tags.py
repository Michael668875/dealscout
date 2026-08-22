from django import template

register = template.Library()


@register.simple_tag
def elided_page_range(page_obj):
    return page_obj.paginator.get_elided_page_range(page_obj.number)