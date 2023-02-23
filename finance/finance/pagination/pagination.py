from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "limit"

    def get_paginated_response(self, data):
        return Response(
            {
                "pagination": {
                    "count": self.page.paginator.count,
                    "page": self.page.number,
                    "limit": self.get_page_size(self.request),
                    "pages": self.page.paginator.num_pages,
                },
                "data": data,
                "info": {"error": ""},
            }
        )
