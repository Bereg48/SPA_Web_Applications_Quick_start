from rest_framework import serializers
from main.models import Habit


from .models import User  # pragma: no cover


class HabitSerializers(serializers.ModelSerializer):
    """Класс HabitSerializers сериализует данные полученные в соответствии с установленной моделью класса Habit,
    данные сериализуются, в рамках функциональности CRUD"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=None)


    def validate_time_required(self, value):
        if value > 120:
            raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд")
        return value

    def validate_associated_habit(self, value):
        if value and not value.pleasant:
            raise serializers.ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки")
        return value

    def create(self, validated_data):
        user = validated_data.get('user')
        associated_habit = validated_data.get('associated_habit')
        reward = validated_data.get('reward')
        time_required = validated_data.get('time_required')
        pleasant = validated_data.get('pleasant')
        frequency = validated_data.get('frequency')

        if not isinstance(user, User):
            raise serializers.ValidationError("user должен быть объектом Users")

        if associated_habit and reward:
            raise serializers.ValidationError("Невозможно одновременно выбрать связанную привычку и вознаграждения")

        if time_required:
            validated_data['time_required'] = self.validate_time_required(time_required)

        if pleasant and (associated_habit or reward):
            raise serializers.ValidationError("Приятная привычка не может иметь связанной с ней привычки или вознаграждения")

        if frequency > 7:
            raise serializers.ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")

        return super().create(validated_data)

    class Meta:  # pragma: no cover
        model = Habit
        fields = '__all__'

