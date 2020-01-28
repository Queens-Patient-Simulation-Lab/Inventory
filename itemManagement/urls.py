from django.urls import path

from itemManagement.views import LocationView
from . import views

urlpatterns = [
    path('item/<int:itemId>', views.sampleItem, name="item-details"),
    path('home/', views.homePage, name="homepage"),
    path('locations/', LocationView.as_view(), name="location-list"),
    path('locations/<int:id>/', LocationView.as_view(), name="location-list")
]
