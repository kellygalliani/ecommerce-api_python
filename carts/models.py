from django.db import models

class Cart(models.Model):
    class Meta:
        ordering = ("id",)

    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    items = models.IntegerField(default=0)

    products = models.ManyToManyField(
        "products.Product",
        related_name="cart",
        through="carts.CartProducts",
        null=True,
        blank=True
    )


class CartProducts(models.Model):
    cart_id = models.ForeignKey("carts.Cart", on_delete=models.CASCADE)
    product_id = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)