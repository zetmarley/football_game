from django.contrib import admin
from main.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team', 'role',
                    'cl', 'age', 'country', 'cost')
    search_fields = ('id', 'name', 'team', 'role',
                    'cl', 'age', 'country', 'cost')