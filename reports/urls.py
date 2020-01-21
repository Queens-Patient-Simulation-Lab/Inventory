from django.urls import path
from . import views

urlpatterns = [
    path('OnHand', views.InventoryOnHand, name="inventory-on-hand")
]
