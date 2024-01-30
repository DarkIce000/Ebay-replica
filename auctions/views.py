from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .formsTemplate import formCreate, formComment, formWatchlist
from .models import User, list_item, comment, watchlist, bid
from django.contrib.auth.decorators import login_required
import datetime

#index page for listing all the items
def index(request):
    listItem = list_item.objects.all()
    return render(request, "auctions/index.html", {
        "listItem": listItem
    })


# create a list on the site
@login_required(login_url="/login")
def createListing(request):
    #getting the submitted data after the user is submitted
    if request.method == "POST":
        listing = formCreate(request.POST)

        if listing.is_valid():
            title = listing.cleaned_data["title"]
            url = listing.cleaned_data["url"]
            description = listing.cleaned_data["Description"]
            initialBid = listing.cleaned_data["initialBid"]

            bidding = bid(initialBid = initialBid)
            bidding.save()

            listItem = list_item(
                product_title = title,
                description=description,
                seller=request.user,
                imageUrl=url,
                bids=bidding
                )
            listItem.save()

        else:
            return render(request, "auctions/createListing.html",{
                "form": formCreate(initial={
                    "title":title,
                    "description": description,
                    "url":url,
                    "initialBid":initialBid
                    })
            })

    return render(request, "auctions/createListing.html", {
        "form": formCreate
    })


#getting the products from db
def product(request, product_id):
    product = list_item.objects.get(id=product_id)
    try:
        get_comments = comment.objects.filter(product_id=product_id)
    except:
        get_comments = "No Comments"
    
#some workaround for the js part handling and watchlist that i didnot know 
# how to make that checkbox checked from fetching from the db

    try: 
        is_in_watchlist= watchlist.objects.get(userId=request.user, product_id=product) 
    except:
        is_in_watchlist = None
    
    if is_in_watchlist :
        is_in_watchlist = "checked"
    else: 
        is_in_watchlist = "unchecked"

    return render(request, "auctions/productPage.html",{
        "product_info": product,
        "add_watchlist": formWatchlist(),
        "formComment":formComment(),
        "display_comments": get_comments, 
        "is_in_watchlist": is_in_watchlist
    })


#commenting feature onthe product page
def commentMade(request, product_id):
    commentobj = formComment(request.POST)
    get_product = list_item.objects.get(id = product_id)
    if request.method == "POST":
        if commentobj.is_valid():
            comment_title = commentobj.cleaned_data['title']
            comment_msg = commentobj.cleaned_data["msg"]

			#saving to the comment table
            comment_save = comment(title=comment_title, msg=comment_msg, product_id=get_product)
            comment_save.save()
            return HttpResponseRedirect(reverse("product_page",args=(product_id,)))

        return HttpResponseRedirect(reverse("product_page", args=(product_id,)), {
            "message" : "comment is invalid"
            })

    return HttpResponseRedirect(reverse("index"))


#watchlist implementation
@login_required(login_url="/login")
def watchList(request, product_id ):

    try:
        watchlist_obj = watchlist.objects.get(userId=request.user, product_id=product)
    except:
        watchlist_obj = None
    
    product = list_item.objects.get(id=product_id)
    if request.method == "POST":
        # if marked in watchlist checkbox then add to the db
        if(request.POST.get('addToWatchlist') and not watchlist_obj):
            add_to_watchlist = watchlist(userId=request.user, product_id=product)
            print('fetching done')
            add_to_watchlist.save()
        #if exits and unchecked then  remove 
        else:
           watchlist_obj .delete() 
        return HttpResponseRedirect(reverse("product_page", args=(product_id,)))

    return HttpResponseRedirect(reverse("product_page", args=(product_id,)))

@login_required(login_url='/login')
def make_bid(request, product_id):
    try: 
        get_product = list_item.objects.get(id=product_id)    
    except:
        get_product = None 

    if request.method == "POST":
        if get_product: 
            get_product.bids.last_bid.update(last_bid=request.POST.get('last_bid'))
            get_product.bids.last_bidder.update(last_bidder=request.POST.get('last_bidder'))



















def login_view(request):

    next = ""
    if request.GET:
        next = request.GET['next']

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            if next is not "":
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html", {
            "next" : next
        })


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