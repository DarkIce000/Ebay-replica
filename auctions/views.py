from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User 
from django.contrib.auth.decorators import login_required




class formCreate(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-control-sm"}))
    Description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"class":"form-control"}))
    url = forms.CharField(label="URL of Image (optional)", widget=forms.TextInput(attrs={"class":"form-control form-control-sm"}))
    category = forms.CharField(label="Category", widget=forms.TextInput(attrs={ "class" : "form-control form-control-sm"}) ) 
    

def index(request):  
    return render(request, "auctions/index.html") 

@login_required
def createListing(request):
    # if request.method == "POST":
    #     f.save()
    return render(request, "auctions/createListing.html", {
        "form": formCreate
    })

def product(request):
    return render(request, "auctions/productPage.html")

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
