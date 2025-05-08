from main.parsing import players_parsing
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Команда создания суперпользователя"""

    def handle(self, *args, **options):
        players_parsing()
