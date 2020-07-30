from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


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
    upload = models.FileField(upload_to='uploads/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    is_active = models.BooleanField(default=True)
    created_at = models.DateField()
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, default="", blank=True, related_name="user")

    @property
    def max_price(self):
       return  Bid.objects.filter(auction=self).aggregate(Max('price'))['price__max']

    def __str__(self):
        return f"{self.name} {self.description} {self.price}"


class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="auction_bid")
    price = models.DecimalField(max_digits=19, decimal_places=10)

    def __str__(self):
        return f"{self.auction} {self.price}"


class Comment(models.Model):
    comment = models.CharField(max_length=300)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} {self.auction}"
