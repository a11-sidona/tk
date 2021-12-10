from django.db.utils import InternalError
from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.http import response
from .models import *
from django.db import connection
import datetime
from django.contrib import messages
# Create your views here.

def index(request):
     with connection.cursor() as cursor:
         
        print({request.session.get("username")})
         
        cursor.execute(f""" 
                SELECT * FROM PENGGALANG_DANA
                WHERE email = '{request.session.get("username")}'
                        """)
         
         
        penggalangDana = cursor.fetchall()
        print(penggalangDana)
        
        cursor.execute(f""" 
                SELECT * FROM PENGGALANGAN_DANA_PD pd JOIN KATEGORI_PD k
                ON pd.email_user = '{request.session.get("username")}' AND pd.id_kategori = k.id
                        """)
        
        penggalanganDana = cursor.fetchall()
        print(penggalanganDana)
        
        cursor.execute(f""" 
                SELECT pd.id, pd.judul, k.nama_kategori FROM PENGGALANGAN_DANA_PD pd JOIN  wishlist_donasi w
                ON pd.id = w.idPd AND w.email = '{request.session.get("username")}' JOIN KATEGORI_PD k
                ON pd.id_kategori = k.id
                        """)
        
        wishlist = cursor.fetchall()

        cursor.execute(f""" 
                SELECT COUNT(pd.id) FROM PENGGALANGAN_DANA_PD pd JOIN  wishlist_donasi w
                ON pd.id = w.idPd AND w.email = '{request.session.get("username")}'
                        """)
        jumlah_wishlist = cursor.fetchall()[0][0]
    
        return render(request, 'profilePengguna.html', {'penggalangDana':penggalangDana, 'penggalanganDana':penggalanganDana, 'wishlist':wishlist, 
                        'jumlah_wishlist' : jumlah_wishlist})

def pencairanDana(request):
    with connection.cursor() as cursor:
        
    # role = request.session['role']
        
        # return redirect('pencairanDana')
        
        if request.method == "GET":
            
            return redirect(request, "formPencairan.html")
            
            # cursor.execute(f""" 
            #         SELECT p.saldo_dona_pay, pd.judul, pd.id FROM PENGGALANG_DANA p JOIN PENGGALANGAN_DANA_PD pd
            #         ON email LIKE 'pwhiskin1@360.cn' and p.email = pd.email_user
            #                 """)
            # penggalangDana = cursor.fetchall()
            # print(penggalangDana)
            # nominals = request.POST.get('nominal')
            # print(nominals)
            
            
            
            # return render(request, 'formPencairan.html', {'penggalangDana':penggalangDana})
        
        else:
            cursor.execute(f""" 
                    SELECT p.saldo_dona_pay, pd.judul, pd.id FROM PENGGALANG_DANA p JOIN PENGGALANGAN_DANA_PD pd
                    ON email LIKE '{request.session.get("username")}' and p.email = pd.email_user
                            """)
            penggalangDana = cursor.fetchall()
            print(penggalangDana)
            nominals = request.POST.get('nominal')
            
            
            
            
            return render(request, 'formPencairan.html', {'penggalangDana':penggalangDana})
            
            
        
            # nominals = request.POST.get('nominal')
            
            # print(nominals)
            # deskripsi = request.POST.get('deskripsi')
            # print(deskripsi)
            # timestamp = datetime.datetime.now()
            # print(timestamp)
            # idpd = request.POST.get('idPd')
            # print(idpd)
            # return render(request, 'formPencairan.html', {'penggalangDana':penggalangDana})
            # cursor.execute(
            #         f"""
            #         INSERT INTO RIWAYAT_PENGGUNAAN_DANA VALUES ('{idpd}','{timestamp}','{nominals}','{deskripsi}')
            #         """
            #     )
            
            
            
            
            # cursor.execute(f""" 
            #         SELECT p.saldo_dona_pay, pd.judul, pd.id FROM PENGGALANG_DANA p JOIN PENGGALANGAN_DANA_PD pd
            #         ON email LIKE 'pwhiskin1@360.cn' and p.email = pd.email_user
            #                 """)
        
        
            
        
        
        
            
        
        
    
    
    return render(request, "formPencairan.html")



def cairDana(request):
    with connection.cursor() as cursor:
        
            try:
                
                nominals = request.POST.get('nominal')
                    
                # print(nominals)
                
                deskripsi = request.POST.get('deskripsi')
                # print(deskripsi)
                
                timestamp = datetime.datetime.now()
                
                # print(timestamp)
                
                idpd = request.POST.get('idPd')
                # print(idpd)
                
                cursor.execute(
                            f"""
                            INSERT INTO RIWAYAT_PENGGUNAAN_DANA VALUES ('{idpd}','{timestamp}','{nominals}','{deskripsi}')
                            """
                        )
                
                cursor.execute(f""" 
                        SELECT p.saldo_dona_pay, pd.judul, pd.id FROM PENGGALANG_DANA p JOIN PENGGALANGAN_DANA_PD pd
                        ON email LIKE '{request.session.get("username")}' and p.email = pd.email_user
                                """)
                penggalangDana = cursor.fetchall()
            
                messages.success(request, "Pencairan berhasil !")
                return render(request, 'formPencairan.html', {'penggalangDana':penggalangDana})
                
            except InternalError:
                messages.warning(request,"Saldo DonaPay mu kurang, pastikan saldo mencukupi nominal pencairan dana")
                cursor.execute(f""" 
                        SELECT p.saldo_dona_pay, pd.judul, pd.id FROM PENGGALANG_DANA p JOIN PENGGALANGAN_DANA_PD pd
                        ON email LIKE '{request.session.get("username")}' and p.email = pd.email_user
                                """)
                penggalangDana = cursor.fetchall()
                return render(request, 'formPencairan.html', {'penggalangDana':penggalangDana})
            
            
        
        # except InternalError:
            # try:
            
                # messages.warning(request,"Saldo DonaPay mu kurang, pastikan saldo mencukupi nominal pencairan dana")
                # return render(request, 'formPencairan.html', {'penggalangDana':penggalangDana})
            # except TypeError:
            #     messages.WARNING(request,"Saldo DonaPay mu kurang, pastikan saldo mencukupi nominal pencairan dana")
            #     return render(request, 'formPencairan.html', {'penggalangDana':penggalangDana})
        
         
    

def detailPenggalangan(request):
    with connection.cursor() as cursor:
        # cursor.execute(f""" 
        #         SELECT * FROM PENGGALANGAN_DANA_PD pd JOIN KATEGORI_PD k
        #         ON pd.email_user = '{request.session.get("username")}' AND pd.id_kategori = k.id
        #                 """)
        
        cursor.execute(f""" 
                SELECT * FROM PENGGALANGAN_DANA_PD pd JOIN KATEGORI_PD k
                ON pd.email_user = '{request.session.get("username")}' AND pd.id_kategori = k.id
                        """)
        
        penggalanganDana = cursor.fetchall()
        print(request.session.get("username"))
        print(penggalanganDana)
        
        cursor.execute(f""" 
                SELECT pd.jumlah_terkumpul,p.nik , p.nama, pk.penyakit, c.komorbid
                FROM PENGGALANGAN_DANA_PD pd JOIN PD_KESEHATAN pk
                ON pd.id = '{penggalanganDana[0][0]}' AND pd.id = pk.idPD JOIN PASIEN p
                ON pk.idPasien = p.nik JOIN KOMORBID c
                ON pd.id = c.idPD
                        """)
        
        kesehatan = cursor.fetchall()
        print(kesehatan)
        
        cursor.execute(f""" 
                SELECT pd.jumlah_terkumpul, r.nosertifikat, kr.nama
                FROM PENGGALANGAN_DANA_PD pd JOIN PD_RUMAH_IBADAH pr
                ON pd.id = '{penggalanganDana[0][0]}' AND pd.id = pr.idPD JOIN RUMAH_IBADAH r
                ON pr.idRumahIbadah = r.nosertifikat JOIN KATEGORI_AKTIVITAS_PD_RUMAH_IBADAH kr
                ON pr.idAktivitas = kr.id
                        """)
        
        rumahIbadah = cursor.fetchall()
        
        cursor.execute(f""" 
                SELECT *
                FROM RIWAYAT_PENGGUNAAN_DANA
                WHERE idpd = '{penggalanganDana[0][0]}'
                        """)
        
        riwayat = cursor.fetchall()
        print(riwayat)
        
    
        return render(request, 'DetailPenggalangan.html', {'penggalanganDana':penggalanganDana, 'kesehatan': kesehatan, 'rumahIbadah':rumahIbadah, 'riwayat':riwayat})
        
    
    
    
     


     
