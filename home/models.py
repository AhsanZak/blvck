from django.db import models
from django.contrib.auth.models import User
from accounts.models import *


# Create your models here.
# class UserDetails(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=200, null=True)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    user_image = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.user_image.url
        except:
            url = ''
        return url


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True)
    total_price = models.IntegerField(null=True, blank=True)
    order_status = models.CharField(max_length=50, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True, blank=True)
    payment_mode = models.CharField(max_length=50, null=True)
    payment_status = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(null=True, blank=True)


class OrderItem(models.Model):
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.product_price * self.quantity
        return total
