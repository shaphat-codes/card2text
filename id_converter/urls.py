
from django.contrib import admin
from django.urls import path
from extractor.views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/v1/extract', UploadCard, name = "upload card"),
]
