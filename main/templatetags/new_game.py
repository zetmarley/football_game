from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def new_game(context):
    """Удаляет ключ из сессии."""
    request = context.get('request')
    if request.session['user']:
        del request.session['user']
    return ""
