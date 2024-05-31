from rest_framework import pagination


class OutlinePaginator(pagination.PageNumberPagination):
    page_size = 1


class CommentPaginator(pagination.PageNumberPagination):
    page_size = 5
