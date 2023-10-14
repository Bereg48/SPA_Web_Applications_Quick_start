from django.contrib import admin

from main.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Класс HabitAdmin для отображения, фильтрации и поиска модели Habit"""
    list_display = ('public', 'time_required', 'reward', 'frequency',
                    'associated_habit', 'pleasant', 'action', 'time', 'place', 'user')
    list_filter = ('user',)
    search_fields = ('public',)


