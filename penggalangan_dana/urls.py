from django.urls import path

from . import views

app_name = "penggalangan_dana"

urlpatterns = [
    path("", views.daftar_penggalangan, name="daftar"),
    path("admin", views.daftar_penggalangan_admin, name="daftar_admin"),
    path("update", views.form_update, name="form_update"),
]
