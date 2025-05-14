from django import template

register = template.Library()


@register.filter(name='last_name')
def last_name(name):
    data = name.split(' ')
    data.remove(data[0])
    if len(data) == 0:
        result = ''
    else:
        result = ' '.join(data)
    return result
