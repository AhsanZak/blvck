from django.db import models


# Create your models here.

class UserDetail(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=150, null=True)
    username = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    pin_code = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)


class Category(models.Model):
    category_name = models.CharField(max_length=50, null=True)


class ProductDetail(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    product_description = models.TextField(null=True)
    product_price = models.IntegerField(null=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.product_image.url
        except AttributeError:
            url = ''
        return url
