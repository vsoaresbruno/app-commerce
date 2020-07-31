from django.contrib import admin

# Register your models here.
from .models import Category, Listing, Comment, Bid, Wishlist

admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Wishlist)
