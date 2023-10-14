from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError

from rest_framework.test import APITestCase  # pragma: no cover
from users.models import User  # pragma: no cover
from .models import Habit  # pragma: no cover
from .serializers import HabitSerializers  # pragma: no cover


class HabitTestCase(APITestCase):  # pragma: no cover
    """Класс HabitTestCase тестирует функциональности CRUD"""

    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='454125')
        self.client.force_authenticate(user=self.user)
        self.habit_data = {
            'user': self.user.id,
            'place': 'Home',
            'time': '12:00:00',
            'action': 'Exercise',
            'pleasant': False,
            'frequency': 2,
            'time_required': 30
        }

    def test_habit_create(self):
        """Тестирование создание привычек"""
        response = self.client.post('/habits/create/', self.habit_data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habit_update(self):
        """Тестирование обновление привычек"""
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)
        habit = Habit.objects.create(user=self.user, place='Gym', time='18:00:00', action='Workout', pleasant=False,
                                     frequency=3, time_required=60)
        updated_data = {
            'user': self.user.id,
            'place': 'Home',
            'time': '12:00:00',
            'action': 'Exercise',
            'pleasant': False,
            'frequency': 2,
            'time_required': 30
        }
        response = self.client.put(f'/habits/update/{habit.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_list(self):
        """Тестирование просмотра привычек"""
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)
        Habit.objects.create(user=self.user, place='Home', time='12:00:00', action='Exercise', pleasant=False,
                             frequency=2, time_required=30)
        Habit.objects.create(user=self.user, place='Gym', time='18:00:00', action='Workout', pleasant=False,
                             frequency=3, time_required=60)
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_public_habit_list(self):
        """Тестирование просмотра публичных привычек"""
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)
        Habit.objects.create(user=self.user, place='Home', time='12:00:00', action='Exercise', pleasant=False,
                             frequency=2, time_required=30, public=True)
        Habit.objects.create(user=self.user, place='Gym', time='18:00:00', action='Workout', pleasant=False,
                             frequency=3, time_required=60)
        response = self.client.get('/public_habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_habit(self):
        """Тестирование просмотра отдельных привычек"""
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)
        habits = Habit.objects.create(user=self.user, place='Home', time='12:00:00', action='Exercise', pleasant=False,
                                      frequency=2, time_required=30, public=True)
        # Отправка GET запроса для получения информации о конкретном объекте Habit
        response = self.client.get(f'/habits/{habits.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_habit(self):
        """Тестирование удаления привычек"""
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)
        habits = Habit.objects.create(user=self.user, place='Home', time='12:00:00', action='Exercise', pleasant=False,
                                      frequency=2, time_required=30)

        # Отправка DELETE запроса для удаления конкретного объекта Habit
        response = self.client.delete(f'/habits/delete/{habits.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class HabitSerializers_time_required_APITestCase(APITestCase):  # pragma: no cover
    """Класс HabitSerializers_time_required_APITestCase тестирует валидацию сереалайзера, а именно поля time_required"""

    def test_validate_time_required_valid_value(self):
        """Метод  test_validate_time_required_valid_value проверяем, что метод
        `validate_time_required` возвращает значение `value`, если оно меньше или равно 120."""
        serializer = HabitSerializers()
        validated_data = serializer.validate_time_required(60)
        self.assertEqual(validated_data, 60)

    def test_validate_time_required_invalid_value(self):
        """Метод test_validate_time_required_invalid_value проверяет,
        что при передаче значения `value`, которое больше 120, метод вызывает `serializers.ValidationError`
        и возвращает сообщение об ошибке "Время выполнения должно быть не больше 120 секунд"."""
        serializer = HabitSerializers()
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.validate_time_required(150)
        self.assertEqual(cm.exception.detail[0], "Время выполнения должно быть не больше 120 секунд")


class HabitSerializers_associated_habit_APITestCase(APITestCase):  # pragma: no cover
    """Класс HabitSerializers_associated_habit_APITestCase тестирует валидацию сереалайзера, а именно поля associated_habit"""

    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='454125')
        self.client.force_authenticate(user=self.user)

    def test_validate_associated_habit_valid_value(self):
        """Метод test_validate_associated_habit_valid_value проверяет, что метод `validate_associated_habit` возвращает
        значение `value`, если оно является объектом `Habit` и имеет признак приятной привычки."""
        serializer = HabitSerializers()
        associated_habit = Habit.objects.create(user=self.user, place='Home', time='12:00:00', action='Exercise',
                                                pleasant=True,
                                                frequency=2, time_required=30)
        validated_data = serializer.validate_associated_habit(associated_habit)
        self.assertEqual(validated_data, associated_habit)

    def test_validate_associated_habit_invalid_value(self):
        """Метод test_validate_associated_habit_valid_value проверяет, что при передаче значения `value`, которое
        является объектом `Habit`, но имеет признак неприятной привычки, метод вызывает `serializers.ValidationError`
        и возвращает сообщение об ошибке "В связанные привычки могут попадать только привычки с признаком приятной привычки"."""
        serializer = HabitSerializers()
        associated_habit = Habit.objects.create(user=self.user, place='Home', time='12:00:00', action='Exercise',
                                                pleasant=False,
                                                frequency=2, time_required=30)
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.validate_associated_habit(associated_habit)
        self.assertEqual(cm.exception.detail[0],
                         "В связанные привычки могут попадать только привычки с признаком приятной привычки")

    def test_validate_associated_habit_empty_value(self):
        """Метод test_validate_associated_habit_empty_value проверяет, что при передаче значения `value`,
        равного `None`, метод возвращает `None` без вызова `serializers.ValidationError`"""
        serializer = HabitSerializers()
        validated_data = serializer.validate_associated_habit(None)
        self.assertIsNone(validated_data)


class HabitSerializers_create_APITestCase(APITestCase):  # pragma: no cover
    """Класс HabitSerializers_create_APITestCase тестирует валидацию сереалайзера, а именно поля associated_habit"""

    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='454125')
        self.client.force_authenticate(user=self.user)

    def test_create_valid_data(self):
        """Метод test_create_valid_data проверяет, что при передаче значения `frequency`, большего 7,
        метод вызывает `serializers.ValidationError` и возвращает сообщение об ошибке "Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
        serializer = HabitSerializers()

        validated_data = {
            'user': self.user,
            'place': 'Home',
            'time': '12:00:00',
            'action': 'Exercise',
            'associated_habit': None,
            'reward': None,
            'time_required': 3,
            'pleasant': True,
            'frequency': 8,
        }

        try:
            serializer.create(validated_data)
        except ValidationError as e:
            self.assertEqual(str(e.detail[0]), "Нельзя выполнять привычку реже, чем 1 раз в 7 дней")
        else:
            self.fail("ValidationError not raised")

    def test_create_associated_habit_and_reward(self):
        """Метод test_create_associated_habit_and_reward проверяет, что при передаче одновременно
        значения `associated_habit` и `reward`, метод вызывает `serializers.ValidationError` и возвращает
        сообщение об ошибке "Невозможно одновременно выбрать связанную привычку и вознаграждения"."""
        serializer = HabitSerializers()
        associated_habit = Habit.objects.create(user=self.user, place='Home', time='12:00:00', action='Exercise',
                                                pleasant=True,
                                                frequency=2, time_required=30)
        reward = "Вознаграждение 1"
        validated_data = {
            'user': self.user,
            'place': 'Home',
            'time': '12:00:00',
            'action': 'Exercise',
            'associated_habit': associated_habit,
            'reward': reward,
            'time_required': 3,
            'pleasant': False,
            'frequency': 7,
        }
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.create(validated_data)
        self.assertEqual(cm.exception.detail[0], "Невозможно одновременно выбрать связанную привычку и вознаграждения")

    def test_create_pleasant_with_associated_habit_or_reward(self):
        """Метод test_create_pleasant_with_associated_habit_or_reward проверяет, что при передаче
        значения `pleasant` равного `True`, а также значения `associated_habit` или `reward`, метод
        вызывает `serializers.ValidationError` и возвращает сообщение об ошибке "Приятная привычка не может иметь
        связанной с ней привычки или вознаграждения"."""
        serializer = HabitSerializers()
        associated_habit = Habit.objects.create(user=self.user, place='Home_2', time='12:00:00', action='Exercise',
                                                pleasant=True,
                                                frequency=2, time_required=30)
        reward = "Вознаграждение 2"
        validated_data = {
            'user': self.user,
            'place': 'Home_2',
            'time': '12:00:00',
            'action': 'Exercise',
            'associated_habit': associated_habit,
            'reward': reward,
            'time_required': 3,
            'pleasant': True,
            'frequency': 4,
        }
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.create(validated_data)
            self.assertTrue(cm.exception.detail[0].startswith(
                "Приятная привычка не может иметь связанной с ней привычки или вознаграждения"))

    def test_create_valid_data_no_errors(self):
        """Метод test_create_valid_data_no_errors проверяет, что при передаче всех входных данных валидации
        проходят успешно и метод создаёт объект `Habit` в БД"""
        serializer = HabitSerializers()
        validated_data = {
            'user': User.objects.get(id=self.user.id),
            'place': 'Home_3',
            'time': '12:00:00',
            'action': 'Exercise',
            'associated_habit': None,
            'reward': None,
            'time_required': 3,
            'pleasant': True,
            'frequency': 4,
        }
        habit = serializer.create(validated_data)
        self.assertIsNotNone(habit)
        self.assertEqual(habit.time_required, 3)
        self.assertTrue(habit.pleasant)
        self.assertEqual(habit.frequency, 4)
