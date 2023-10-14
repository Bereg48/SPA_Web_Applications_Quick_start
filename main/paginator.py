from rest_framework.pagination import PageNumberPagination


class PageNumberPagination(PageNumberPagination):
    """Класс MainPaginator является пагинаторм который, определяет количество объектов на одной странице,
    он наследуется от класса PageNumberPagination"""
    page_size = 5  # Количество объектов на каждой странице
    page_query_param = 'page'  # Параметр запроса для номера страницы
    page_size_query_param = 'page_size'  # Параметр запроса для количества объектов на странице
    max_page_size = 100  # Максимальное количество объектов на странице
