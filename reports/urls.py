from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.sampleReport, name="sample-report")
]
