from rest_framework.pagination import PageNumberPagination


class DynamicPageSizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_page_size(self, request):
        # Determine admin using custom flag with fallback to Django's built-in
        is_admin = False
        if request.user.is_authenticated:
            is_admin = getattr(request.user, 'is_super_user', False) or getattr(request.user, 'is_superuser', False)
        if is_admin:
            requested_size = request.query_params.get(self.page_size_query_param)
            if not requested_size and request.method == 'POST' and hasattr(request, 'data'):
                requested_size = request.data.get(self.page_size_query_param)
            if requested_size:
                try:
                    return min(int(requested_size), self.max_page_size)
                except (ValueError, TypeError):
                    pass
            return self.max_page_size
        requested_size = request.query_params.get(self.page_size_query_param)
        if not requested_size and request.method == 'POST' and hasattr(request, 'data'):
            requested_size = request.data.get(self.page_size_query_param)
        if requested_size:
            try:
                return min(int(requested_size), 10)
            except (ValueError, TypeError):
                pass
        return 10