from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionList(models.Model):
    Item = models.CharField(max_length=30)
    Item_current_price = models.IntegerField(default=0)
    Creator_name = models.CharField(max_length=30)
    Item_description = models.CharField(max_length=500)
    Created_date=models.DateTimeField()
    Item_photo = models.ImageField()
    Category=models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.Item

class Bids(models.Model):
    Item=models.ForeignKey(AuctionList,on_delete=models.CASCADE)
    Item_price=models.IntegerField()
    Bidder_name=models.CharField(default="Not defined",max_length=50)

    def __str__(self) :
        return f"{self.Item} "
    
   
class Watchlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    Item=models.ForeignKey(AuctionList, on_delete=models.CASCADE)

    def __str__(self) :
        return f"{self.user} || {self.Item} "

 
class Comments(models.Model):
    Item = models.ForeignKey(AuctionList,on_delete=models.CASCADE,)
    Commenter=models.ForeignKey(User,on_delete=models.CASCADE,default="undefined")
    Item_comment = models.CharField(max_length=300,default="")

    def __str__(self) :
        return f"{self.Item} || Commentor:{self.Commenter} "
