from django.shortcuts import render


def home(request):
    return render(request, "main/home.html")


def penggalangan_dana(request):
    return render(request, "main/penggalangan.html")
