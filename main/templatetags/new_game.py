from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def new_game(context):
    """Удаляет ключ из сессии."""
    request = context.get('request')
    session_key = request.session.session_key
    if request.session[session_key]:
        del request.session[session_key]
    return ""
