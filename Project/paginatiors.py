from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 10

    # the get_paginated_response method overrides the default one in the PageNumberPagination class and this modified version modifies the response headers to add the "count", "next_page" and "previous_page" attributes in the header else the default one adds these attributes to the response body.
    def get_paginated_response(self, data):
        response = Response(data)
        response['count'] = self.page.paginator.count
        response['next_page'] = self.get_next_link()
        response['previous_page'] = self.get_previous_link()
        return response
