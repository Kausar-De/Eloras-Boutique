from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name = "register"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),

    #path('', views.homepage, name = "homepage"),
    path('', views.store, name = "store"),
    path('product/<str:pk>/', views.product, name = "product"),
    path('removeitem/<str:pk>/', views.removeItem, name = "removeitem"),
    path('myorders/', views.myOrders, name = "myorders"),
    
    path('cart/', views.cart, name = "cart"),
    path('checkout/', views.checkout, name = "checkout"),

    path('emailtemplate/', views.emailtemplate, name = "emailtemplate"),
]