from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/listing", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.listing_by_category, name="listing_by_category"),
    path("comments", views.comments, name="comments"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid", views.place_bid, name="place_bid"),
    path("close_bid", views.close_bid, name="close_bid"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)