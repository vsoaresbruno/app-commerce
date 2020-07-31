from datetime import datetime
from typing import List

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing, Bid, Comment, Wishlist
from .forms import ListingForm
 
def index(request):
    active_listing = Listing.objects.all().filter(is_active=True)
    
    return render(request, "auctions/index.html", {
        "listings_list": active_listing
    })

def listings(request, id):
    listing = Listing.objects.get(id=id)
    current_price = Bid.objects.filter(auction=id).aggregate(Max('price'))
    price = current_price['price__max'] or listing.price
    comments = Comment.objects.all().filter(auction=listing)
    wishlist = False
    
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(auction=listing, user=request.user).exists()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": price,
        "comments": comments,
        "wishlist": wishlist
    })

def categories(request):
    categories_list = Category.objects.all().order_by('name')

    return render(request, "auctions/categories.html", {
        "categories_list": categories_list
    })

def listing_by_category(request, category_id):
    listings_list = Listing.objects.all().filter(category=category_id)
    
    return render(request, "auctions/index.html", {
        "listings_list": listings_list
    })

@login_required
def comments(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        auction_id = request.POST.get('id')
        auction = Listing.objects.get(id=auction_id)
        try:
            comment = Comment(comment= comment, auction=auction)
            comment.save()
        except IntegrityError:
            pass

    return HttpResponseRedirect(reverse("listings", args=[auction_id]))

@login_required
def wishlist(request):
    if request.method == "POST":
        auction_id = request.POST.get('id')
        auction = Listing.objects.get(id=auction_id)
        wishlist = Wishlist.objects.filter(auction=auction, user=request.user)

        if wishlist.exists():
            wishlist.delete()
            return HttpResponseRedirect(reverse("listings", args=[auction_id]))
        else:
            new_wishlist = Wishlist(auction= auction, user=request.user)
            new_wishlist.save()
            return HttpResponseRedirect(reverse("listings", args=[auction_id]))

    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            product_name = form.cleaned_data['product_name']
            product_description = form.cleaned_data['product_description']
            product_starting_bid = format(form.cleaned_data['product_starting_bid'], '.2f')
            product_category = form.cleaned_data['product_category']
            product_image = request.FILES.get('product_image', None)
            category = Category.objects.get(id=product_category)
            created_at = datetime.now()

            try:
                listing = Listing(name=product_name, description=product_description, price=product_starting_bid,
                                    category=category, upload=product_image, created_at=created_at, listed_by=user)
                listing.save()
                #return HttpResponseRedirect('/thanks/')
            except IntegrityError:
                return render(request, 'auctions/create_listing.html', {
                    "message": "Try Again"
                })
    else:
        form = ListingForm()

    return render(request, 'auctions/create_listing.html', {
        'form': form,
        'categories': categories
    })
