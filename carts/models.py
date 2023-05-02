from django.db import models
import uuid


class Cart(models.Model):
    class Meta:
        ordering = ("id",)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    items = models.IntegerField(default=0)

    products = models.ManyToManyField(
        "products.Product",
        related_name="cart",
        null=True,
        blank=True
    )
    