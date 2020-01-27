from django.urls import path
from . import views

urlpatterns = [
    path('locations/', views.locationList, name="location-list")
]