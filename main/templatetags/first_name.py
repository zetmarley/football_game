from django import template

register = template.Library()


@register.filter(name='first_name')
def first_name(name):
    data = name.split(' ')
    result = data[0]
    return result
