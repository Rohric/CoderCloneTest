from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """Paginator for the offer list with a configurable page_size query parameter."""

    page_size = 6
    page_size_query_param = "page_size"

    def get_page_size(self, request):
        raw = request.query_params.get(self.page_size_query_param)
        if raw is not None:
            try:
                return int(raw)
            except ValueError:
                raise ValidationError({"page_size": "Must be an integer."})
        return self.page_size
