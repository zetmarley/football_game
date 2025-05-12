import os
import random
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from config.settings import BASE_DIR
from main.forms import PlayerForm
from main.models import Player


def set_session_value(request):
    # request.session['user'] = {'hidden_player': random.choice(Player.objects.all()),
    request.session['user'] = {'hidden_player': Player.objects.get(name='Marc Guéhi'),
                               'selected_players': [],
                               'attempts': 8,
                               'show_dialog': False}
    return HttpResponse("Session value set")


def get_session_values(request):
    user = request.session.get('user')
    return user


def new_game(request):
    if request.session['user']:
        del request.session['user']


class GameView(TemplateView):
    template_name = f"{BASE_DIR}/main/templates/game.html"

    def get(self, request, *args, **kwargs):
        if not get_session_values(request):
            set_session_value(request)
        context = self.get_context_data(**kwargs)
        context['selected_players'] = request.session['user']['selected_players']
        context['hidden_player'] = request.session['user']['hidden_player']
        context['attempts'] = request.session['user']['attempts']
        context['show_dialog '] = request.session['user']['show_dialog']
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if not get_session_values(request):
            set_session_value(request)
            return render(request, self.template_name, context)
        else:
            selected_player = Player.objects.get(name=request.POST.get('footballer'))
            selected_players = request.session.get('user')['selected_players']
            if request.session['user']['hidden_player'] != selected_player:
                selected_players.append(selected_player)
                request.session['user']['selected_players'] = selected_players
                request.session['user']['attempts'] -= 1
                request.session.save()
            else:
                selected_players.append(selected_player)
                request.session['user']['selected_players'] = selected_players
                request.session.save()

            context['hidden_player'] = request.session['user']['hidden_player']
            context['selected_players'] = request.session['user']['selected_players']
            context['attempts'] = request.session['user']['attempts']
            context['show_dialog '] = request.session['user']['show_dialog']

            return render(request, self.template_name, context)


def autocomplete(request):
    if 'term' in request.GET:
        term = request.GET['term']
        footballers = Player.objects.filter(name__icontains=term)[:10]
        results = [{'id': f.id, 'label': f.name} for f in footballers]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)
