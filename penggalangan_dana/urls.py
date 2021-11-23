from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.daftar_penggalangan, name="daftar_penggalangan"),
    path("admin", views.daftar_penggalangan_admin, name="daftar_penggalangan_admin"),
]
