from django.shortcuts import render
from django.db import connection
from django.contrib import messages 
from django.db import IntegrityError

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

    # with connection.cursor() as cursor:
    #     print({request.session.get("username")})

    #     cursor.execute(f""" 
    #             SELECT * FROM PENGGALANG_DANA
    #             WHERE email = '{request.session.get("username")}'
    #                     """)
    with connection.cursor() as cursor:
        cursor.execute(f""" 
                SELECT D.idpd, PD.judul, K.nama_kategori, S.status
                FROM DONASI D, PENGGALANGAN_DANA_PD PD, KATEGORI_PD K, STATUS_PEMBAYARAN S
                WHERE D.email = '{request.session.get("username")}' AND D.idpd = PD.id
                AND PD.id_kategori = K.id AND D.idstatuspembayaran = S.id
                        """)
        list_donasi = cursor.fetchall()
        print(list_donasi)

        return render(request, "data_donasi.html", {"list_donasi" : list_donasi})


    return render(request, "data_donasi.html")

def form_donasi(request):
    with connection.cursor() as cursor:

        if request.method == "GET":

            print({request.session.get("username")})

            cursor.execute(f""" 
                    SELECT P.email, PD.judul FROM PENGGALANG_DANA P, WISHLIST_DONASI W, PENGGALANGAN_DANA_PD PD
                    WHERE P.email = '{request.session.get("username")}'
                    AND P.email = W.email AND PD.id = W.idpd
                            """)

            penggalangDana = cursor.fetchall()
            print(penggalangDana)
            email_form = penggalangDana[0]
            judul_form = penggalangDana[0]
            print(penggalangDana[0])
            print(penggalangDana[0][0])
            print(judul_form[1])

            return render(request, "form_donasi.html", {'email_form' : email_form[0], 'judul_form' : judul_form[1]})
            # return render(request, "form_donasi.html", {'data_form' : penggalangDana})
        
        else:
            print(request.POST)
            with connection.cursor() as cursor:
                cursor.execute(f""" 
                    SELECT id FROM PENGGALANGAN_DANA_PD
                    WHERE judul = '{request.POST["judul"]}'
                            """)
                id_penggalangan = cursor.fetchall()[0][0]
                # print(id_penggalangan)
                # print(request.POST["email"])

                cursor.execute(f"""
                        INSERT INTO donasi VALUES
                        ('{request.POST["email"]}', '{request.POST["timestamp"]}', '{request.POST["nominal"]}','{request.POST["bayar"]}',
                        '{request.POST["anonim"]}', '{request.POST["doa"]}', '{id_penggalangan}', 924491011)
                    """)
                return render(request, "detail_donasi.html")




    # return render(request, "form_donasi.html")

def detail_donasi(request):
    return render(request, "detail_donasi.html")