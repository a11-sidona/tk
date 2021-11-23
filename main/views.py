from django.shortcuts import render


def home(request):
    return render(request, "main/home.html")


def daftar_penggalangan(request):
    return render(request, "main/daftar_penggalangan.html")

def daftar_penggalangan_admin(request):
    return render(request, "main/admin/daftar_penggalangan.html")
