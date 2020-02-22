from django.urls import path

from kghDataManagement.views import KghUploadPage
from . import views

URL_KGH_UPLOAD_PAGE = "kgh-upload"


urlpatterns = [
    path('', KghUploadPage.as_view(), name=URL_KGH_UPLOAD_PAGE)
]
