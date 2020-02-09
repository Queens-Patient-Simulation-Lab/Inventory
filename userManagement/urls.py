from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings, name="settings-home"),
    path('user_account/', views.userAccount, name="user-account"),
    path('user_register/', views.userRegister, name="user-register"),
    path('user_delete/<str:email>/', views.userDelete, name="user-delete"),
    path('user_role/<str:email>/', views.userRole, name="user-role"),
]