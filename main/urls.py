from django.urls import path
from main import views
from main.apps import MainConfig


app_name = MainConfig.name

urlpatterns = [
    path('', views.game, name='game'),
]