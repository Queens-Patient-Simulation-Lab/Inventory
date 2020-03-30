from django.urls import path

from kghDataManagement.views import KghUploadPage
from . import views

URL_KGH_UPLOAD_PAGE = "kgh-upload"
URL_KGH_DOWNLOAD_TEMPLATE = "kgh-download-template"


urlpatterns = [
    path('', KghUploadPage.as_view(), name=URL_KGH_UPLOAD_PAGE),
    path('download-template/', views.downloadKghTemplate, name=URL_KGH_DOWNLOAD_TEMPLATE)
]
