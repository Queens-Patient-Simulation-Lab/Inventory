from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.MainPage, name="reports"),
    re_path(r'^onHand/(?:(?P<format>(?:csv|pdf))/)?$', views.InventoryOnHand, name="inventory-on-hand"),
    re_path(r'^cycle/(?:(?P<format>(?:csv|pdf))/)?$', views.CycleCount, name="cycle-count")
]
