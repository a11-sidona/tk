from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("sukses", views.sukses),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("register-admin", views.register_admin, name="register-admin"),
    path("register-user", views.register_user, name="register-user"),
    path("register-user-individu", views.register_user_individu, name="register-user-individu"),
    path("register-user-organisasi", views.register_user_organisasi, name="register-user-organisasi"),
    path("admin-sidona/list-pengguna", views.list_pengguna_terdaftar, name="list_pengguna"),
    path('logout/',views.logout, name='logout')
]
