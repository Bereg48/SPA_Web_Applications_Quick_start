import logging
from celery.schedules import crontab
from django.utils import timezone
from main.models import Habit
from celery import shared_task
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_LOCAL_ID
from main.telegram_utils import TelegramNotifier

telegram_notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN)

logger = logging.getLogger(__name__)


@shared_task
def remind_habits():
    """Метод remind_habits использует текущее время, чтобы найти все привычки, которые должны быть напомнены
    в данный момент. Затем вызывает задачу `send_habit_notification()` для отправки уведомления для каждой найденной привычки."""
    now = timezone.now().time()
    now_without_seconds = now.replace(second=0)
    time_str = now_without_seconds.strftime('%H:%M:%S')
    habits = Habit.objects.filter(time=time_str)
    print(f"Количество времени {time_str}")
    print(f"Количество привычек{habits}")
    print(f"Количество привычек: {len(habits)}")
    logger.info(f"Количество привычек: {len(habits)}")

    for habit in habits:
        # Вызываем задачу для отправки уведомления
        send_habit_notification.delay(habit.id)

        print(f"Отправлена задача на отправку уведомления для привычки с id {habit.id}")
        logger.info(f"Отправлена задача на отправку уведомления для привычки с id {habit.id}")


@shared_task
def send_habit_notification(habit_id):
    """Метод send_habit_notification отправляет уведомление через `telegram_notifier` с помощью Telegram API.
    Принимает идентификатор привычки `habit_id` и использует его для получения соответствующей привычки из базы данных.
    Затем отправляет уведомление с информацией о привычке и ее времени"""
    habit = Habit.objects.get(pk=habit_id)
    telegram_notifier.send_notification(chat_id=TELEGRAM_CHAT_LOCAL_ID, message=f'Напоминание: {habit.action} в {habit.time}')


@shared_task
def schedule_next_notification(habit_id):
    """Метод schedule_next_notification планирует следующее уведомление для привычки. Принимает идентификатор
    привычки `habit_id`, использует его для получения соответствующей привычки из базы данных. Затем вычисляет
    время следующего уведомления, добавляет один день к текущему времени, и вызывает `remind_habits.apply_async()`
    для запланированного выполнения задачи `remind_habits()` через Celery"""
    habit = Habit.objects.get(pk=habit_id)
    eta = timezone.now() + timezone.timedelta(days=1)
    remind_habits.apply_async(eta=eta, schedule=crontab(hour=habit.time.hour, minute=habit.time.minute))
