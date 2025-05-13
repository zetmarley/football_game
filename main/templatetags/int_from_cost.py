from django import template

register = template.Library()


@register.filter(name='int_from_cost')
def int_from_cost(cost):
    data = cost.split(' ')
    return float(data[0].replace(',', '.'))
