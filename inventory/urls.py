from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="inventory-login"),
    path('home/', views.homePage, name="inventory-homepage")
]
