from django.db import models


class Product(models.Model):

    class Meta:
        ordering = ("id",)

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    availability = models.BooleanField(default=True)
    seller = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="products"
    )
