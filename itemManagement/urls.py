from django.urls import path
from . import views

urlpatterns = [
    path('item/', views.sampleItem, name="sample-item"),
    path('home/', views.homePage, name="homepage"),
]
