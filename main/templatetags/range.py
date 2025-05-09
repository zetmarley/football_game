from django import template


register = template.Library()


@register.filter(name='range')
def range(number):
    return range(number)