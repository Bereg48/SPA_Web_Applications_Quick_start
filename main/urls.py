from django.urls import path

from .apps import MainConfig
from .views import HabitListAPIView, HabitCreateAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, HabitDestroyAPIView, \
    PublicHabitListAPIView

app_name = MainConfig.name

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habit-list'),
    path('public_habits/', PublicHabitListAPIView.as_view(), name='public_habits-list'),
    path('habits/create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-retrieve'),
    path('habits/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('habits/delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit-delete'),

    # path('telegram-webhook/', telegram_webhook, name='telegram-webhook'),
]
