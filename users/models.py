from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    roles = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    def __str__(self):  # pragma: no cover
        return self.roles

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
