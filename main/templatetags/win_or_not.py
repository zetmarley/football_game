from django import template


register = template.Library()


@register.simple_tag(takes_context=True, name='win_or_not')
def win_or_not(context):
    if context['hidden_player'] in context['selected_players']:
        return True
    else:
        return False