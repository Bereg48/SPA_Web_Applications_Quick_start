from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from main.models import Habit
from main.paginator import PageNumberPagination
from main.serializers import HabitSerializers


class HabitListAPIView(generics.ListAPIView):
    """Класс HabitListAPIView отвечает за функциональность просмотра при применении
    класса HabitSerializers, который функционирует в соответствии с определенной моделью класса Habit"""
    queryset = Habit.objects.all().order_by('id')
    serializer_class = HabitSerializers
    pagination_class = PageNumberPagination
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicHabitListAPIView(generics.ListAPIView):
    """Класс PublicHabitListAPIView отвечает за функциональность просмотра публичных привычек при применении
    класса HabitSerializers, который функционирует в соответствии с определенной моделью класса Habit"""
    serializer_class = HabitSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(public=True)


class HabitCreateAPIView(generics.CreateAPIView):
    """Класс HabitCreateAPIView отвечает за функциональность добавления при применении
    класса HabitSerializers, который функционирует в соответствии с определенной моделью класса Habit"""
    serializer_class = HabitSerializers
    permission_classes = [IsAuthenticated]

    # permission_classes = [IsAuthenticated, IsAdminUser | IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Класс HabitRetrieveAPIView отвечает за функциональность просмотра конкретного объекта при применении
        класса HabitSerializers, который функционирует в соответствии с определенной моделью класса Habit"""
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        return Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Класс HabitUpdateAPIView отвечает за функциональность обновление конкретного объекта при применении
        класса HabitSerializers, который функционирует в соответствии с определенной моделью класса Habit"""
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    # permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Класс HabitDestroyAPIView отвечает за функциональность удаления конкретного объекта при применении
            класса LessonSerializers, который функционирует в соответствии с определенной моделью класса Habit"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


