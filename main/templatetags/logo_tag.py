from django import template

from main.models import Logo

register = template.Library()


@register.filter(name='logo_tag')
def logo_tag(team):
    if Logo.objects.filter(team=team).exists():
        return Logo.objects.get(team=team).pic