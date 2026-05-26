from django.db.models import Min, Q
from rest_framework.exceptions import ValidationError


VALID_ORDERING = ["updated_at", "min_price"]


def apply_offer_filters(queryset, params):
    """Apply creator, price, delivery time, ordering, and search filters to an offer queryset."""
    creator_id = params.get("creator_id")
    if creator_id:
        try:
            queryset = queryset.filter(user__id=int(creator_id))
        except ValueError:
            raise ValidationError({"creator_id": "Must be an integer."})

    min_price = params.get("min_price")
    if min_price:
        try:
            queryset = queryset.filter(details__price__gte=float(min_price)).distinct()
        except ValueError:
            raise ValidationError({"min_price": "Must be a number."})

    max_delivery_time = params.get("max_delivery_time")
    if max_delivery_time:
        try:
            queryset = queryset.filter(details__delivery_time_in_days__lte=int(max_delivery_time)).distinct()
        except ValueError:
            raise ValidationError({"max_delivery_time": "Must be an integer."})

    ordering = params.get("ordering")
    if ordering in VALID_ORDERING:
        if "min_price" in ordering:
            queryset = queryset.annotate(min_price_val=Min("details__price")).order_by(
                ordering.replace("min_price", "min_price_val")
            )
        else:
            queryset = queryset.order_by(ordering)

    search = params.get("search")
    if search:
        queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

    return queryset
