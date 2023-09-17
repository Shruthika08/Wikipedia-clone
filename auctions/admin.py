from django.contrib import admin
from .models import AuctionList,User,Bids,Watchlist,Comments
# Register your models here.
admin.site.register(AuctionList)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Watchlist)
admin.site.register(Comments)