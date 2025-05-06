from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Player(models.Model):
    """Модель футбольного игрока"""

    name = models.CharField(unique=True, max_length=70, verbose_name='Игрок')
    team = models.CharField(max_length=50, verbose_name='Команда')
    role = models.CharField(max_length=50, verbose_name='Роль')
    cl = models.IntegerField(verbose_name='ЛЧ')
    age = models.PositiveIntegerField(verbose_name='Возраст')
    country = models.CharField(max_length=50, verbose_name='Страна')
    cost = models.CharField(max_length=50, verbose_name='Цена')


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'