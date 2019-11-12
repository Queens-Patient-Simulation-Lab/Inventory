from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('report/', views.sampleReport, name="sample-report"),
    path('item/', views.sampleItem, name="sample-item"),
    path('home/', views.homePage, name="homepage"),
]
