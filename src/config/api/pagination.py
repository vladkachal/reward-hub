from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data: dict) -> Response:
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class SmallPageNumberPagination(BasePageNumberPagination):
    page_size = 10
    max_page_size = 100


class StandardPageNumberPagination(BasePageNumberPagination):
    page_size = 25
    max_page_size = 100


class LargePageNumberPagination(BasePageNumberPagination):
    page_size = 50
    max_page_size = 200
