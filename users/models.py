from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    class Meta:
        ordering = ("id",)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    is_seller = models.BooleanField(default=False)
    cart = models.OneToOneField(
        "carts.Cart", 
        on_delete=models.CASCADE, 
        related_name="user"
    )
    address = models.OneToOneField(
        "addresses.Address", 
        on_delete=models.CASCADE, 
        related_name="user")
