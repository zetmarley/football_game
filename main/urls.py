from django.urls import path
from main.views import GameView, autocomplete, new_game
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', GameView.as_view(), name='game'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    # path('new_game/', new_game, name='new_game'),

]
