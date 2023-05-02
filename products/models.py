from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    availability = models.BooleanField()
    seller = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="products"
    )
