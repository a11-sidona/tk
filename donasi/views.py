from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "data_donasi.html")

def form_donasi(request):
    return render(request, "form_donasi.html")

def detail_donasi(request):
    return render(request, "detail_donasi.html")