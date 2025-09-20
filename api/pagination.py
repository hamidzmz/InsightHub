from rest_framework.pagination import PageNumberPagination


class DynamicPageSizePagination(PageNumberPagination):
    page_size = 10  # Default for regular users
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_page_size(self, request):
        if request.user.is_authenticated and request.user.is_super_user:
            # For super users, default to 100 unless specified
            requested_size = request.query_params.get(self.page_size_query_param)
            if requested_size:
                try:
                    return min(int(requested_size), self.max_page_size)
                except (ValueError, TypeError):
                    pass
            return 100
        else:
            # For regular users, default to 10 unless specified
            requested_size = request.query_params.get(self.page_size_query_param)
            if requested_size:
                try:
                    return min(int(requested_size), 10)
                except (ValueError, TypeError):
                    pass
            return 10