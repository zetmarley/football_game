import os
import random
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from config.settings import BASE_DIR
from main.forms import PlayerForm
from main.models import Player


def set_session_value(request):
    session_key = request.session.session_key

    request.session[session_key] = {'hidden_player': random.choice(Player.objects.all()),
    # request.session[session_key] = {'hidden_player': Player.objects.get(name="Matt O'Riley"),
    'selected_players': [],
    'attempts': 8,
    'show_dialog': False}
    return HttpResponse("Session value set")


def get_session_values(request):
    session_key = request.session.session_key
    user = request.session.get(session_key)
    return user


def new_game(request):
    session_key = request.session.session_key
    if request.session[session_key]:
        del request.session[session_key]


class GameView(TemplateView):
    template_name = f"{BASE_DIR}/main/templates/game.html"

    def get(self, request, *args, **kwargs):
        if not get_session_values(request):
            set_session_value(request)
        session_key = request.session.session_key
        context = self.get_context_data(**kwargs)
        context['selected_players'] = request.session[session_key]['selected_players']
        context['hidden_player'] = request.session[session_key]['hidden_player']
        context['attempts'] = request.session[session_key]['attempts']
        context['show_dialog '] = request.session[session_key]['show_dialog']
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if not get_session_values(request):
                set_session_value(request)
            session_key = request.session.session_key
            selected_player = Player.objects.get(name=request.POST.get('footballer'))
            selected_players = request.session.get(session_key)['selected_players']
            if request.session[session_key]['hidden_player'] != selected_player:
                selected_players.append(selected_player)
                request.session[session_key]['selected_players'] = selected_players
                request.session[session_key]['attempts'] -= 1
                request.session.save()
            else:
                selected_players.append(selected_player)
                request.session[session_key]['selected_players'] = selected_players
                request.session.save()

            context['hidden_player'] = request.session[session_key]['hidden_player']
            context['selected_players'] = request.session[session_key]['selected_players']
            context['attempts'] = request.session[session_key]['attempts']
            context['show_dialog '] = request.session[session_key]['show_dialog']

            return render(request, self.template_name, context)
        except Player.DoesNotExist:
            session_key = request.session.session_key
            context['selected_players'] = request.session[session_key]['selected_players']
            context['hidden_player'] = request.session[session_key]['hidden_player']
            context['attempts'] = request.session[session_key]['attempts']
            context['show_dialog '] = request.session[session_key]['show_dialog']
            return render(request, self.template_name, context)


def autocomplete(request):
    term = request.GET.get('term', '')
    results = Player.objects.filter(name__icontains=term)[:5]  # Пример запроса
    data = [{'label': f.name, 'id': f.id} for f in results]  # Формат для JS
    return JsonResponse(data, safe=False)
