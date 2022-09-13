from django.contrib import admin
from django.urls import path,include
from authentication import views

urlpatterns = [
    path('',views.index, name = "index"),
    path('register',views.register, name = "register"),
    path('login',views.login, name = "login"),
    path('adminpage',views.adminpage, name = "adminpage"),
    path('userpage',views.userpage, name = "userpage"),
    path('changepassword',views.changepassword, name = "changepassword"),
    path('applyleave',views.applyleave, name = "applyleave"),
]
