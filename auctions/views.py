from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, list_item
from django.contrib.auth.decorators import login_required


#form for the create page  

class formCreate(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control my-2 form-control-sm", "name":"title"}))
    Description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"class":"form-control my-2", "name":"description"}))
    url = forms.CharField(label="URL of Image (optional)", widget=forms.TextInput(attrs={"class":"form-control my-2 form-control-sm", "name":"url", "type":"url"}))
    category = forms.CharField(label="Category", widget=forms.TextInput(attrs={ "class" : "form-control form-control-sm my-2", "name":"category"}) ) 
    

def index(request):  
    listItem = list_item.objects.all()
    
    return render(request, "auctions/index.html", {
        "listItem": listItem 
    }) 

def createListing(request):
    #getting the submitted data after the user is submitted 
    if request.method == "POST":
        if formCreate.is_valid:
            title = formCreate.cleaned_data["title"]
            url = formCreate.cleaned_data["url"]
            description = formCreate.create_data["description"]
            listItem = list_item(product_title = title, description=description, seller=request.user.id, imageUrl=url)
            listItem.save()
        else:
            return render(request, "auctions/createListing.html",{
                "form": formCreate(initial={"title":title, "description": description, "url":url})
            })

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
