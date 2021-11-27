from django.urls import path

from . import views

app_name = "penggalangan_dana"

urlpatterns = [
    path("", views.daftar_penggalangan, name="daftar"),
    path("admin", views.daftar_penggalangan_admin, name="daftar_admin"),
    path("PD", views.daftar_penggalangan_PD, name="daftar_PD"),
    path("update", views.form_update, name="form_update"),
    path("form_verifikasi", views.form_verifikasi, name="form_verifikasi"),
    path("detail", views.detail_penggalangan),
    path("komorbid", views.komorbid, name="komorbid"),
    path("komorbid/tambah", views.komorbid_tambah, name="komorbid_tambah"),
    path("komorbid/update", views.komorbid_update, name="komorbid_update"),
    path("create", views.create_PD_category, name="create_PD_category"),
    path("create/cekpasien", views.cek_pasien, name="cek_pasien"),
    path("create/cekrumah", views.cek_rumah, name="cek_rumah"),
    path("create/daftarrumah", views.daftar_rumah, name="daftar_rumah"),
    path("create/daftarpasien", views.daftar_pasien, name="daftar_pasien"),
    path("create/form_PD", views.form_PD, name="form_PD"),
    path("kategori/tambah", views.form_tambah_kategori),
    path("kategori/", views.list_kategori),
    path("kategori/update", views.form_update_kategori),
]
