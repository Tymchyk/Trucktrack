from django.urls import path
from . import views


urlpatterns =[
    path('',views.index, name ="index"),
    path('login', views.logining, name = "login"),
    path('register',views.register, name="register"),
    path('logout',views.logouting, name="logout"),
    path('neworder', views.neworder, name="neworder"),
    path('orders_map', views.orders_map, name ="orders_map"),
    path('order/<int:id>', views.order, name="order"),
    path('profile/<int:id>', views.profile_page, name="profile"),
    path('myorders', views.my_orders, name="myorders"),
    path('rating/<int:id>', views.rating, name = "rating"),
    path("chat", views.chat, name="chat"),
    path('chats/<int:id>', views.chats, name="chats"),
    path('profileorders',views.profile_orders, name="profileorders"),
    path('orderstart/<int:id>', views.orderstart, name="orderstart")
]