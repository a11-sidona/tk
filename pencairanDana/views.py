from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import response
from .models import *
# Create your views here.

def index(request):
    # pengguna = 
    return render(request, "profilePengguna.html")

def pencairanDana(request):
    # context = {}

    # form = NoteForm(request.POST or None, request.FILES or None)

    # if form.is_valid():
    #     form.save()
    #     return redirect('/lab-4')

    # context['form'] = form
   return render(request, "formPencairan.html")

def detailPenggalangan(request):
     return render(request, "DetailPenggalangan.html")


     
