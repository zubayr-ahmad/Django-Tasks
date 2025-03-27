# pagination.py
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination
from rest_framework.response import Response
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5  
    max_limit = 30 

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'  # documentation says it has to be set to use max_page_size
    max_page_size = 50

class TimeBasePagination(CursorPagination):
    page_size = 7
    ordering = '-published_date'

class MetaDataPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    
    def get_paginated_response(self, data):
        return Response({
            'metadata': {
                'total_items': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
            },
            'results': data
        })


