from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings, name="settings-home"),
    path('change_password/', views.change_password, name="change-password"),
    path('notification/', views.notification, name="notification"),
]