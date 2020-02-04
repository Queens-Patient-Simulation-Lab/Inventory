from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.MainPage, name="reports"),
    re_path(r'^onHand/(?:(?P<format>(?:csv|pdf))/)?$', views.InventoryOnHand, name="inventory-on-hand"),
    re_path(r'^obsolecense/(?:(?P<format>(?:csv|pdf))/)?$', views.InventoryObsolescence, name="inventory-obsolecense"),
    re_path(r'^reorder/(?:(?P<format>(?:csv|pdf))/)?$', views.ReorderList, name="reorder"),
    re_path(r'^valuation/(?:(?P<format>(?:csv|pdf))/)?$', views.InventoryValuation, name="valuation"),
    path('cycle/', views.CycleCountHTML, name="cycle-count"),
    path('cycle/csv', views.CycleCountCSV, name="cycle-count-csv"),
    path('cycle/pdf', views.CycleCountPDF, name="cycle-count-pdf")
]
