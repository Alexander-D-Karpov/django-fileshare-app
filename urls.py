from django.urls import path

from .api.views import UploadFileViewSet
from .views import *

urlpatterns = [
    path("", file_list, name="file.index"),
    path("<str:slug>", view_file, name="file_view"),
    path("delete_file/<str:slug>", delete_file, name="delete_file"),
    path("group/<str:slug>", group, name="file_group"),
    path(
        "upload/", UploadFileViewSet.as_view({"post": "file"}), name="file.api.upload"
    ),
]
