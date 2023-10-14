from rest_framework import serializers

from users.models import User


class UserSerializers(serializers.ModelSerializer):
    """Класс LessonSerializers сериализует данные полученные в соответствии с установленной моделью класса Lesson,
    данные сериализуются, в рамках функциональности CRUD"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = User
        fields = '__all__'