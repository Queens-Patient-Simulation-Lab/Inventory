from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:itemId>', views.sampleItem, name="item-details"),
    path('home/', views.homePage, name="homepage"),
]
