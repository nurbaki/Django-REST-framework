from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 15 # size oer page
    page_query_param="sayfa" # page seklinde degilde , sayfa seklinde link olusturur
    page_size_query_param="limit" # url'ye limit komutuyla page size belirtmek icin kullanilir


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50
    limit_query_param = 'adet'  # Defaults to 'limit'.
    offset_query_param = 'haric'

class MycursorPagination(CursorPagination):
    page_size=10
    ordering = "first_name"