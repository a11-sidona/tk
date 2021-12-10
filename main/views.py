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

def login(request):
    return render(request, "login/login.html")

def register(request):
    return render(request, "login/register.html")

def register_admin(request):
    return render(request, "login/register_admin.html")

def register_user(request):
    
    
    
    
    return render(request, "login/register_user.html")

def register_user_individu(request):
    return render(request, "login/individu.html")

def register_user_organisasi(request):
    return render(request, "login/organisasi.html")

def list_pengguna_terdaftar(request):
    return render(request, "admin/list_pengguna.html")