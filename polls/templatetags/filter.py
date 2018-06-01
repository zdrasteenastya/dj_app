from json import loads

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def json(value):
    return mark_safe(', '.join(answer.encode('utf-8') for answer in loads(value)))
