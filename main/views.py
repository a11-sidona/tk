from django.http import response
from django.shortcuts import redirect, render


def home(request):
    if request.method == "POST":
        nama = request.POST["nama"]

        response = {}
        response["nama"] = nama
        return render(request, "main/next.html", response)

    return render(request, "main/home.html")


def sukses(request):
    if request.method == 'POST':
        response = {}
        response['nama'] = request.POST['nama']
        response['alamat'] = request.POST['alamat']
        return render(request, "main/sukses.html", response)

    return redirect('/')
