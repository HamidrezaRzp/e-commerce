from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = '"products"."categories"'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100,
                                   unique=True,
                                   blank=False,
                                   null=False,)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    seller = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               limit_choices_to={'role': 'seller'},
                               related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        db_table = '"products"."products"'

    def __str__(self):
        return self.name
    
    def get_stock(self):
        if self.stock>0 :return f'availabe quantity :{self.stock}'
        else : return 'not available'

    def clean(self):
        if self.seller.role != 'seller':
            raise ValidationError('Assigned user mut have seller role!')
