from django import template

from main.models import Flag

register = template.Library()


@register.filter(name='flag_tag')
def flag_tag(country):
    if Flag.objects.filter(country=country).exists():
        return Flag.objects.get(country=country).pic