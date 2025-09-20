from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from django.db.models import UniqueConstraint


User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('cart')
        verbose_name_plural = ('carts')

    def __str__(self):
        return f"Cart {self.id} for {self.user.email}"


class CartItme(models.Model):
    cart = models.ForeignKey(Cart,
                                on_delete=models.CASCADE,
                                related_name='cartitems')
    product = models.ForeignKey(Product,
                                   on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["cart", "product"], name="unique_cart_item_per_prodct")
        ]

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart:{self.cart.id}"
