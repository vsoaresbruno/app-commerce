from django.contrib import admin

# Register your models here.
from .models import Category, Listing, Comment, Bid

admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
