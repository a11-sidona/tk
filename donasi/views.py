from django.shortcuts import render
from django.db import connection

# Create your views here.
def index(request):
    # cursor = connection.cursor()
    # cursor.execute('SET SEARCH_PATH TO SIDONA;')
    # # butuh dapetin email dari pengguna skarang biar bisa nampilin donasi khusus punya dia
    # cursor.execute("""
    #                 SELECT D.idpd, PD.judul, K.nama_kategori, S.status
    #                 FROM PENGGALANGAN_DANA PD, KATEGORI_PD K, STATUS_PEMBAYARAN S, DONASI D
    #                 WHERE D.idpd = PD.id AND PD.id_kategori = K.id AND
    #                 D.id_status_pembayaran = S.id;
    #                 """)
    # list_donasi = cursor.fetchall()
    # response = {"list_donasi" : list_donasi}

    return render(request, "data_donasi.html")

def form_donasi(request):
    return render(request, "form_donasi.html")

def detail_donasi(request):
    return render(request, "detail_donasi.html")