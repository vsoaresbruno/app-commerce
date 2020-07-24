from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    upload = models.FileField(upload_to='uploads/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  blank=True, related_name="category")
    is_active = models.BooleanField(default=True)
    created = models.DateField()

    def __str__(self):
        return f"{self.name} {self.description} {self.price}"


class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=10)

    def __str__(self):
        return f"{self.auction} {self.price}"


class Comment(models.Model):
    comment = models.CharField(max_length=300)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} {self.auction}"
