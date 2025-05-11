from django import template


register = template.Library()


@register.filter(name='make_list')
def make_list(number):
    failed_attempts = 8 - number

    result = [1 for _ in range(failed_attempts)]

    while len(result) != 8:
        result.append(0)
    return result