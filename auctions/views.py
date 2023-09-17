from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.fields import CharField, JSONString
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import User,AuctionList,Bids,Comments,Watchlist
import datetime
class createlist(forms.Form):
    item_name=forms.CharField(label="Item name",max_length= 50)
    creator_name=forms.CharField(label="Creator name",max_length=30)
    item_description=forms.CharField(label="Item Description",max_length=500)
    item_start_price = forms.IntegerField(label="Start price")
    item_photo =forms.ImageField()
    


def index(request):
    bids=dict()
    Item_list=AuctionList.objects.all()

    for item in Item_list:
        if request.user.username is not '':
             user=User.objects.get(username=request.user.username)
             isbookmarked=Watchlist.objects.filter(user=user,Item=item).exists()
        else:
            isbookmarked=False
        bids[item.Item]={"current_bid":Bids.objects.get(Item=item).Item_price,
                    "bidder_name":Bids.objects.get(Item=item).Bidder_name,
                    "Item":item.Item,
                    "Creator_name":item.Creator_name,
                    "Category":item.Category,
                    "isbookmarked":isbookmarked,
                    "Item_description":item.Item_description,
                    "Created_date":item.Created_date,
                    "Item_photo":item.Item_photo,
                    "Item_current_price":item.Item_current_price
        }
    print(bids)
    return render(request, "auctions/index.html",{
        "ActiveList":bids,
        "Bids":bids,
        "message":"No items please create items"
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

def watchlist(request):
    if request.user.username is not '':
        user=User.objects.get(username=request.user.username)
        watchlist=Watchlist.objects.filter(user=user)
        bids=dict()
        Item_list=AuctionList.objects.all()

        for item in watchlist:
            
           bids[item.Item.Item]={"current_bid":Bids.objects.get(Item=item.Item).Item_price,
                        "bidder_name":Bids.objects.get(Item=item.Item).Bidder_name,
                        "Item":item.Item,
                        "Creator_name":item.Item.Creator_name,
                        "Category":item.Item.Category,
                        "isbookmarked":True,
                        "Item_description":item.Item.Item_description,
                        "Created_date":item.Item.Created_date,
                        "Item_photo":item.Item.Item_photo,
                        "Item_current_price":item.Item.Item_current_price
            }
        print(bids)
        return render(request, "auctions/watchlist.html",{
            "watchlist":bids,
            "Bids":bids
        })

       

def addwatchlist(request,item_name):
    item=AuctionList.objects.get(Item=item_name)
    if request.user.username is not '':
        user=User.objects.get(username=request.user.username)
        if not Watchlist.objects.filter(user=user,Item=item).exists():
            Watchlist.objects.create(user=user,Item=item)
        else:
            Watchlist.objects.get(user=user,Item=item).delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        bids=dict()
        Item_list=AuctionList.objects.all()

        for item in Item_list:
            if request.user.username is not '':
                user=User.objects.get(username=request.user.username)
                isbookmarked=Watchlist.objects.filter(user=user,Item=item).exists()
            else:
                isbookmarked=False
            bids[item.Item]={"current_bid":Bids.objects.get(Item=item).Item_price,
                        "bidder_name":Bids.objects.get(Item=item).Bidder_name,
                        "Item":item.Item,
                        "Creator_name":item.Creator_name,
                        "Category":item.Category,
                        "isbookmarked":isbookmarked,
                        "Item_description":item.Item_description,
                        "Created_date":item.Created_date,
                        "Item_photo":item.Item_photo,
                        "Item_current_price":item.Item_current_price
            }
        print(bids)
        return render(request, "auctions/index.html",{
            "ActiveList":bids,
            "Bids":bids,
            "message":"No items please create",
            "messagelog":"Please login to add to watchlist"
        })
        
        

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



def create_listing(request):
    categories=AuctionList.objects.values("Category")
    if(request.method =="POST"):
        print(request.POST)
        item_name = request.POST["item_name"]
        item_description = request.POST["item_description"]
        item_start_price = request.POST["start_price"]
        item_creator_name=request.POST["creator_name"]
        item_photo=request.FILES["item_image"]
        category=request.POST["Category"]
        create_date=datetime.datetime.now()
        print(f"Item name is {item_name}|| Item description: {item_description} || Item start price:{item_start_price} || Creator name :{item_creator_name} ")
        Item = AuctionList.objects.create(Item=item_name,Item_current_price=item_start_price,Item_description=item_description,
        Creator_name=item_creator_name,Created_date=create_date, Item_photo=item_photo,Category=category)
        
        Bid=Bids.objects.create(Item=Item,Item_price=item_start_price,Bidder_name=item_creator_name)
        
        
        return HttpResponseRedirect(reverse("index") )

    
    else:
        return render(request,"auctions/creatlisting.html",{
            "catagories":categories,
            "message":None,

        })


def itemdisp(request,item_name):
    Item=AuctionList.objects.get(Item=item_name)
    Bid=Bids.objects.get(Item=Item).Bidder_name
    if request.user.username is not '':
        if Watchlist.objects.filter(user=User.objects.get(username=request.user.username), Item=Item).exists():
            isbookmarked=True
        else:
            isbookmarked=False
    else:
        isbookmarked=False
    if Comments.objects.filter(Item=Item).exists():
        comment=Comments.objects.filter(Item=Item)
    else:
        comment=None
    return render(request,"auctions/item.html",{
        "Item":Item,
        "highest_bidder":Bid,
        "isbookmarked":isbookmarked,
        "comments":comment
    })

def updatebid(request):
   item_name = request.POST['item_name']
   updated_price=request.POST['new_price']
   highest_bidder=Bids.objects.get(Item=AuctionList.objects.get(Item=item_name))
   highest_bidder=highest_bidder.Bidder_name
   if request.user.username is not '': 
        
        Item=AuctionList.objects.get(Item=item_name)
        item=Bids.objects.get(Item=AuctionList.objects.get(Item=item_name))
        if int(updated_price)>item.Item_price:
            item.Item_price=int(updated_price)
            item.Bidder_name=request.user.username
            Item.Item_current_price=updated_price
            Item.save()
            item.save()
        else:
            return render(request,"auctions/item.html",{
                "Item":AuctionList.objects.get(Item=item_name),
                "message":"Please Login!!",
                "highest_bidder":highest_bidder,
                "messageper":"Bid made should have higher value than previous bid"
            })
        
        return HttpResponseRedirect(reverse("index"))
   else:
       return render(request,"auctions/item.html",{
           "Item":AuctionList.objects.get(Item=item_name),
           "highest_bidder":highest_bidder,
           "message":"Please login!!"
       })

def closebid(request,item_name):
    item=AuctionList.objects.get(Item=item_name)
    creator_name=item.Creator_name
    if request.user.username == creator_name:
        highest_bidder = Bids.objects.get(Item=item).Bidder_name
        AuctionList.objects.get(Item=item_name).delete()
        return render(request,"auctions/item.html",{
            "Item":item,
          
           "messageclosebid":highest_bidder
        })
    else:
        highest_bidder = Bids.objects.get(Item=item).Bidder_name
        return render(request,"auctions/item.html",{
            "Item":AuctionList.objects.get(Item=item_name),
           "message":"Please login!!",
           "messageclosebid":highest_bidder
        })
    
def categories(request):
    category_list = AuctionList.objects.values("Category").distinct()
    return render(request,"auctions/categories.html",{
        "categories":category_list
    })

def categorylist(request,category):
    bids=dict()
    Item_list=AuctionList.objects.filter(Category=category)

    for item in Item_list:
        if request.user.username is not '':
             user=User.objects.get(username=request.user.username)
             isbookmarked=Watchlist.objects.filter(user=user,Item=item).exists()
        else:
            isbookmarked=False
        bids[item.Item]={"current_bid":Bids.objects.get(Item=item).Item_price,
                    "bidder_name":Bids.objects.get(Item=item).Bidder_name,
                    "Item":item.Item,
                    "Creator_name":item.Creator_name,
                    "Category":item.Category,
                    "isbookmarked":isbookmarked,
                    "Item_description":item.Item_description,
                    "Created_date":item.Created_date,
                    "Item_photo":item.Item_photo,
                    "Item_current_price":item.Item_current_price
        }
    print(bids)
    return render(request, "auctions/categoryitem.html",{
        "ActiveList":bids,
        "Bids":bids,
        "category":category,
        "message":"No items please create items"
    })
def comment(request):
    username=request.user.username
    item_name=request.POST["item"]
    if request.method=="POST":
        item=AuctionList.objects.get(Item=request.POST["item"])
    if User.objects.filter(username=username).exists():
        Comments.objects.create(Item=item,Commenter=User.objects.get(username=username),Item_comment=request.POST["comment"])
        return HttpResponseRedirect(f"/{item_name}")