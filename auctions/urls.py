from django.urls import path

from . import views
# app_name = "auction"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("comment",views.comment,name="comment"),
    path("categories",views.categories,name="categories"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("createlist",views.create_listing,name="createlisting"),
    path("updatebid",views.updatebid,name="updatebid"),
    path("categories/<str:category>",views.categorylist,name="categoryitemlist"),
    path("closebid/<str:item_name>",views.closebid,name="closebid"),
    path("addwatchlist/<str:item_name>",views.addwatchlist,name="addwatchlist"),
    
    path("<str:item_name>",views.itemdisp,name="itemdisp"),
    
]
