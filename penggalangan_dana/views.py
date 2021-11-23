from django.shortcuts import render


def daftar_penggalangan(request):
    return render(request, "penggalangan/daftar_penggalangan.html")


def daftar_penggalangan_admin(request):
    return render(request, "penggalangan/admin/daftar_penggalangan.html")

def form_update(request):
    return render(request, "penggalangan/form_update.html")