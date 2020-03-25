from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings, name="settings-home"),
    path('user_account/', views.userAccount, name="user-account"),
    path('user_register/<uidb64>/<token>/', views.userRegister, name="user-register"),
    path('forget_password/', views.forgetPassword, name="forget-password"),
    path('forget_password_confirm/<uidb64>/<token>/', views.forgetPasswordConfirm, name="forget-password-confirm"),
    path('user_delete/<str:email>/', views.userDelete, name="user-delete"),
    path('user_admin/<str:email>/', views.userAdmin, name="user-admin"),
    path('user_labAssistant/<str:email>/', views.userLabAssistant, name="user-lab-assistant"),
]