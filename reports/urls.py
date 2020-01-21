from django.urls import path
from . import views

urlpatterns = [
    path('OnHand', views.InventoryOnHand, name="inventory-on-hand"),
    path('cycle', views.CycleCount, name="cycle-count")
]
