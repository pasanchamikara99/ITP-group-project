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
    path('applyleave/<id>',views.applyleave, name = "applyleave"),
    #path('generatepdf',views.generatepdf, name = "generatepdf"),
    path('update_emp/<id>',views.update_emp, name = "update_emp"),
    path('delete_emp/<id>',views.delete_emp, name = "delete_emp"),
    path('updateuser',views.updateuser, name = "updateuser"),
    path('leaves',views.leaves, name = "leaves"),
    path('approve_leave/<id>',views.approve_leave, name = "approve_leave"),
    path('reject_leave/<id>',views.reject_leave, name = "reject_leave"),
    path('addNewLeave',views.addNewLeave, name = "addNewLeave"),
    path('addNewEmpPosition',views.addNewEmpPosition, name = "addNewEmpPosition"),
    path('printFile',views.printFile, name = "printFile"),
    path('delete_leave/<id>',views.delete_leave, name = "delete_leave"),
    path('delete_position/<id>',views.delete_position, name = "delete_position"),
    path('logout',views.logout, name = "logout"),
]
