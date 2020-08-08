from datetime import datetime
from typing import List

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing, Bid, Comment, Watchlist
from .forms import ListingForm

def index(request):
    active_listing = Listing.objects.all().filter(is_active=True)

    return render(request, "auctions/index.html", {
        "listings_list": active_listing
    })

def listings(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    max_bid = Bid.objects.filter(auction=listing_id).aggregate(Max('price'))
    price = max_bid['price__max'] or listing.price
    comments = Comment.objects.all().filter(auction=listing)
    watchlist = False
    winner_bidder = ''
    
    highst_bid = Bid.objects.filter(auction=listing_id)
    if highst_bid:
        winner_bidder = highst_bid.latest('id').user


    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(auction=listing, user=request.user).exists()
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": price,
        "comments": comments,
        "watchlist": watchlist,
        "winner_bidder": winner_bidder
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
def create_listing(request):
    categories = Category.objects.all()
    form = ListingForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.listed_by = request.user
        # faltou aquele auto_now_add
        instance.created_at = datetime.now()
        instance.save()
        return HttpResponseRedirect(reverse("listings", args=[instance.id]))
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'auctions/create_listing.html', context)

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
def watchlist(request):
    if request.method == "POST":
        auction_id = request.POST.get('id')
        auction = Listing.objects.get(id=auction_id)
        watchlist = Watchlist.objects.filter(auction=auction, user=request.user)

        if watchlist.exists():
            watchlist.delete()
            return HttpResponseRedirect(reverse("listings", args=[auction_id]))
        else:
            new_watchlist = Watchlist(auction= auction, user=request.user)
            new_watchlist.save()
            return HttpResponseRedirect(reverse("listings", args=[auction_id]))
    
    watchlist = Watchlist.objects.filter(user=request.user)

    watchlist_ids = (
        Watchlist.objects
        .filter(user=request.user)
        .values_list('auction_id', flat=True)
    )  

    listing = Listing.objects.filter(id__in=watchlist_ids)

    return render(request, "auctions/watchlist.html", {
        "listings_list": listing
    })

@login_required
def place_bid(request):
    if request.method == "POST":
        bid_requested = float(request.POST.get("bid"))
        auction_id = request.POST.get('id')
        listing = Listing.objects.get(id=auction_id)
        last_bid = Bid.objects.filter(auction=auction_id).aggregate(Max('price'))['price__max']
        bid = Bid(auction=listing, price=bid_requested, user=request.user)
       
        if last_bid and bid_requested > last_bid:
            bid.save()
        elif not last_bid and bid_requested > listing.price:
            bid.save()
        else:
            messages.error(request, 'Bid need to be bigger than current price.')

        return HttpResponseRedirect(reverse('listings', args=(auction_id)))

    return HttpResponseRedirect(reverse('index'))

def close_bid(request):
    if request.method == 'POST':
        auction_id = request.POST.get('id')
        Listing.objects.filter(id=auction_id).update(is_active=False)
        
        return HttpResponseRedirect(reverse('listings', args=(auction_id)))

    return HttpResponseRedirect(reverse('index'))

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
