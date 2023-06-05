
from django.contrib import admin
from django.urls import path
from extractor.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('card/upload', UploadCard, name = "upload card"),
]
