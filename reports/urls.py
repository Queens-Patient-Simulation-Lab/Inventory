from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.MainPage, name="reports"),
    re_path(r'^onHand/(?:(?P<format>(?:csv|pdf))/)?$', views.InventoryOnHand, name="inventory-on-hand"),
    path('cycle/', views.CycleCountHTML, name="cycle-count"),
    path('cycle/csv', views.CycleCountCSV, name="cycle-count-csv"),
    path('cycle/pdf', views.CycleCountPDF, name="cycle-count-pdf")
]
