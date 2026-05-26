# Order model representing a placed service order between a customer and a business.
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from offers_app.models import OfferDetail

User = get_user_model()


class Order(models.Model):
    """
    Captures a snapshot of an OfferDetail at the time of ordering.
    Fields like title, price, and features are copied from the OfferDetail
    so that later edits to the offer do not change historical orders.
    """

    STATUS_CHOICES = [
        ("in_progress", "In Bearbeitung"),
        ("completed", "Abgeschlossen"),
        ("cancelled", "Storniert"),
    ]

    customer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders_as_customer",
    )
    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders_as_business",
    )

    # SET_NULL so that deleting an offer does not cascade to order history.
    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    title = models.CharField(max_length=255, blank=True)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)

    offer_type = models.CharField(max_length=20)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress",
    )

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.title} ({self.status})"
