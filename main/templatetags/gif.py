import random

from django import template

register = template.Library()


@register.filter(name='gif')
def gif(win_or_lose):
    win_list = ['win1.webm', 'win2.webm', 'win3.webm', 'win4.webm']
    lose_list = ['lose1.webm', 'lose2.webm', 'lose3.webm']
    if win_or_lose == 'win':
        return random.choice(win_list)
    elif win_or_lose == 'lose':
        return random.choice(lose_list)
    else:
        return ''
