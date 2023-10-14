from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):  # pragma: no cover
    """Модель Habit"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=100, verbose_name='место выполнения привычки')
    time = models.TimeField(verbose_name='время выполнения привычки', null=True)
    action = models.CharField(max_length=100, verbose_name='действие привычки')
    pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки', null=True)
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                         verbose_name='связанная привычка')
    frequency = models.PositiveIntegerField(default=1, verbose_name='периодичность привычки')
    reward = models.CharField(max_length=100, verbose_name='вознаграждение', **NULLABLE)
    time_required = models.IntegerField(verbose_name='время на выполнение привычки', null=True)
    public = models.BooleanField(default=False, verbose_name="признак публичности")

    def __str__(self):
        return f'{self.place} ({self.time}), {self.action}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['id']
