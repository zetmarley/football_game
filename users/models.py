from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""

    name = models.CharField(max_length=35, verbose_name='имя')
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=12, verbose_name='номер телефона', **NULLABLE)

    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'