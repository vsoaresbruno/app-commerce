from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing
from .forms import ListingForm

def index(request):
    active_listing = Listing.objects.all().filter(is_active=True)
    
    return render(request, "auctions/index.html", {
        "listings_list": active_listing 
    })

def listings(request, id):
    listing = Listing.objects.get(id=id)
    
    return render(request, "auctions/listing.html", {
        "listing": listing 
    })

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
            product_name = form.cleaned_data['product_name']
            product_description = form.cleaned_data['product_description']
            product_starting_bid = format(form.cleaned_data['product_starting_bid'], '.2f')
            product_category = form.cleaned_data['product_category']
            product_image = request.FILES.get('product_image', None)
            category = Category.objects.get(id=product_category)
            created = datetime.now()
            
            listing = Listing(name=product_name, description=product_description, price=product_starting_bid,
                                category=category, image=product_image, created=created)
            listing.save()
            # return HttpResponseRedirect('/thanks/')
    else:
        form = ListingForm()

    return render(request, 'auctions/create_listing.html', {
        'form': form,
        'categories': categories
        })