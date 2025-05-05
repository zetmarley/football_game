import os

from django.shortcuts import render
from config.settings import BASE_DIR


def game(request):
    return render(request, f"{BASE_DIR}/main/templates/game.html")
