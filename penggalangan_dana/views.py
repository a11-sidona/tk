from django.http import response, JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, redirect
from django.db import connection
import penggalangan_dana
import datetime
from random import randrange
from penggalangan_dana.utils import namedtuple_fetch_all



def daftar_penggalangan(request):
    cursor_p = connection.cursor()
    query = """
            SELECT pd.id, judul, kota, provinsi, tanggal_aktif_akhir, sisa_hari, jumlah_dibutuhkan, nama_kategori
            FROM sidona.penggalangan_dana_pd pd, sidona.kategori_pd k
            WHERE pd.id_kategori = k.id AND status_verifikasi = 'Terverifikasi' AND sisa_hari > 0;
            """
    cursor_p.execute(query)
    pds = namedtuple_fetch_all(cursor_p)
    return render(request, "penggalangan/daftar_penggalangan.html", {"pds": pds})


def daftar_penggalangan_admin(request):
    cursor_p = connection.cursor()
    query = """
            SELECT pd.id, judul, kota, provinsi, tanggal_aktif_awal, tanggal_aktif_akhir, sisa_hari, jumlah_dibutuhkan, nama_kategori, status_verifikasi
            FROM sidona.penggalangan_dana_pd pd, sidona.kategori_pd k
            WHERE pd.id_kategori = k.id;
            """
    cursor_p.execute(query)
    pds = namedtuple_fetch_all(cursor_p)
    return render(request, "penggalangan/admin/daftar_penggalangan.html", {"pds": pds})


def daftar_penggalangan_PD(request):
    with connection.cursor() as cursor:
        cursor.execute("select pd.id, pd.judul, pd.kota, pd.provinsi, pd.tanggal_aktif_awal, pd.tanggal_aktif_akhir, pd.sisa_hari, pd.jumlah_dibutuhkan, k.nama_kategori, pd.status_verifikasi from penggalangan_dana_pd pd, penggalang_dana p, kategori_pd k where pd.email_user = p.email and pd.id_kategori=k.id and pd.email_user = %s",[request.session.get("username")])
        result = namedtuple_fetch_all(cursor)
        cursor.execute("select jumlah_pd from penggalang_dana where email=%s",[request.session.get("username")])
        jumlah_pd = cursor.fetchall()[0][0]
        cursor.execute("select jumlah_pd_aktif from penggalang_dana where email=%s",[request.session.get("username")])
        jumlah_pd_aktif = cursor.fetchall()[0][0]
        response ={
            "hasil":result,
            "jumlah":jumlah_pd,
            "aktif":jumlah_pd_aktif
        }
        print(result)
    return render(request, "penggalangan/admin/daftar_PD_pribadi.html", response)


def form_update(request):
    id = request.GET.get("id", "")
    if not id:
        raise SuspiciousOperation("No ID Provided")
    cursor_p = connection.cursor()
    query = (
        """
        SELECT pd.id, pd.judul, pd.deskripsi, pd.kota, pd.provinsi, pd.tanggal_aktif_akhir,
            pd.jumlah_dibutuhkan, pd.status_verifikasi, k.nama_kategori
        FROM penggalangan_dana_pd pd, kategori_pd k
        WHERE id_kategori in (
            SELECT id
            FROM kategori_pd
            WHERE id = pd.id_kategori
        )  AND pd.id = '{}';
        """.format(id)
    )
    cursor_p.execute(query)
    pd = namedtuple_fetch_all(cursor_p)

    response = {
        "pd": pd[0],
    }

    if getattr(pd[0], 'nama_kategori') == 'kesehatan':
        query = (
            """
            SELECT p.nik, p.nama, pdk.penyakit, k.komorbid
            FROM pd_kesehatan pdk, pasien p, komorbid k, penggalangan_dana_pd pdpd
            WHERE k.idpd in (
                SELECT idpd
                FROM komorbid
                WHERE komorbid.idpd = pdpd.id
            ) AND pdk.idpd = '{}' AND pdk.idpasien = p.nik
            """.format(getattr(pd[0], 'id'), getattr)
        )
        cursor_p.execute(query)
        pdk = namedtuple_fetch_all(cursor_p)
        response["pdk"] = pdk
    elif getattr(pd[0], 'nama_kategori') == 'rumah_ibadah':
        pass

    return render(request, "penggalangan/form_update.html", response)


def form_verifikasi(request):
    return render(request, "penggalangan/form_verifikasi.html")


def form_tambah_kategori(request):
    return render(request, "penggalangan/kategori/form_tambah.html")


def list_kategori(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM kategori_pd")
        result = namedtuple_fetch_all(cursor)
        response ={
            "kategoris": result
        }
    return render(request, "penggalangan/kategori/list.html", response)


def form_update_kategori(request):
    response = {}

    if request.method == 'POST':
        id = request.POST["id"]
        nama = request.POST["nama"]
        with connection.cursor() as cursor:
            cursor.execute("UPDATE kategori_pd SET nama_kategori = '{nama}' WHERE id = '{id}';".format(nama=nama, id=id))
            response["message"] = "Sukses mengupdate kategori!"

    id = request.GET.get("id", "")
    if not id: return redirect('/penggalangan/kategori/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM kategori_pd WHERE id = '{}'".format(id))
        result = namedtuple_fetch_all(cursor)
        response["k"] = result[0]

    return render(request, "penggalangan/kategori/form_update.html", response)


def detail_penggalangan(request):
    id = request.GET.get("id", "1")
    response = {"id": id}
    return render(request, "penggalangan/detail_penggalangan.html", response)

def delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("delete from penggalangan_dana_pd where id=%s",[id])
    return redirect("penggalangan_dana:daftar_PD")

def deleteKomorbid(request, id):
    with connection.cursor() as cursor:
        cursor.execute("delete from komorbid where idPD=%s",[id])
    return redirect("penggalangan_dana:komorbid")

def create_PD_category(request):
    with connection.cursor() as cursor:
        cursor.execute("select nama_kategori from sidona.kategori_pd")
        kategori = cursor.fetchall()
        response ={
            "kategori" : kategori,
        }
        if request.method == "POST":
            category = request.POST["category"]

            response = {}
            response["email"]=request.session["username"]
            response["id"] = increment_id_pd(request,category)
            response["category"] = category
            return render(
                request, "penggalangan/create_PD/form_penggalangan_dana.html", response
            )

    return render(request, "penggalangan/create_PD/form_kategori.html", response)

def increment_id_pd(request, kategori):
    with connection.cursor() as cursor:
        user = request.session["username"]
        cursor.execute("select id from penggalangan_dana_pd where email_user=%s order by id desc limit 1",[user])
        newID = cursor.fetchall()
        if(len(newID)>0):
            if(newID[0][0][1]!="-"):
                newID= str(int(newID[0][0])+1)
                newID = kategori[0]+"-"+newID
            else:
                newID= str(int(newID[0][0][2:-1])+1)
                newID = kategori[0]+"-"+newID
        else:
            newID = kategori[0]+"-001"
    return newID


def cek_pasien(request):
    with connection.cursor() as cursor:
        if request.method == "POST":
            nik = request.POST["NIK"]
            cursor.execute("select nik from sidona.pasien where nik = %s", [nik])
            result = cursor.fetchall()
            if(len(result)==0):
                response = {
                    "warning":"gagal"
                }
                return render(request, "penggalangan/create_PD/cek_pasien.html",response)
            response = {}
            response["email"]=request.session["username"]
            cursor.execute("select nama from sidona.pasien where nik = %s", [nik])
            response["category"] = "Kesehatan"
            response["NIK"] = nik
            response["nama"] = cursor.fetchall()
            response["id"] = increment_id_pd(request,"Kesehatan")
            return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/cek_pasien.html")


def cek_rumah(request):
    with connection.cursor() as cursor:
        if request.method == "POST":
            noSertif = request.POST["noSertif"]
            cursor.execute("select nosertifikat from sidona.rumah_ibadah where nosertifikat = %s", [noSertif])
            result = cursor.fetchall()
            if(len(result)==0):
                response = {
                    "warning":"gagal"
                }
                return render(request, "penggalangan/create_PD/cek_rumah_ibadah.html",response)
            response = {}
            response["email"]=request.session["username"]
            response["category"] = "Rumah Ibadah"
            response["noSertif"] = noSertif
            cursor.execute("select nama from sidona.kategori_aktivitas_pd_rumah_ibadah")
            response["kategori"] = cursor.fetchall()
            response["id"] = increment_id_pd(request, "Rumah Ibadah")
            return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/cek_rumah_ibadah.html")


def daftar_pasien(request):
    with connection.cursor() as cursor:
        if request.method == "POST":
            nik = request.POST["NIK"]
            nama = request.POST["Nama"]
            tanggal = request.POST["Tanggal"]
            alamat = request.POST["Alamat"]
            pekerjaan = request.POST["Pekerjaan"]
            cursor.execute("insert into pasien values (%s,%s,%s,%s,%s)",[nik, nama, tanggal, alamat, pekerjaan])
            cursor.execute("select nama from sidona.pasien where nik = %s", [nik])
            response = {}
            response["email"]=request.session["username"]
            response["category"] = "Kesehatan"
            response["NIK"] = nik
            response["nama"] = cursor.fetchall()
            response["id"] = increment_id_pd(request,"Kesehatan")
            return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/form_pasien.html")


def daftar_rumah(request):
    with connection.cursor() as cursor:
        if request.method == "POST":
            noSertif = request.POST["noSertif"]
            nama = request.POST["Nama"]
            alamat = request.POST["Alamat"]
            jenis = request.POST["Jenis"]
            response = {}
            response["email"]=request.session["username"]
            response["category"] = "Rumah Ibadah"
            response["noSertif"] = noSertif
            cursor.execute("select nama from sidona.kategori_aktivitas_pd_rumah_ibadah")
            response["kategori"] = cursor.fetchall()
            cursor.execute("insert into rumah_ibadah values (%s,%s,%s,%s)",[noSertif, nama, alamat, jenis])
            response["id"] = increment_id_pd(request, "Rumah Ibadah")
            return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/form_rumah_ibadah.html")


def form_PD(request):
    with connection.cursor() as cursor:
        response = {}
        email = request.session["username"]
        response["email"] = email
        if request.method == "POST":
            id = request.POST["id"]
            judul = request.POST["judul"]
            deskripsi = request.POST["deskripsi"]
            kota = request.POST["kota"]
            provinsi = request.POST["provinsi"]
            deadline = request.POST["deadline"]
            target = request.POST["target"]
            cursor.execute("select email from admin")
            admin = cursor.fetchall()
            irand = randrange(0, len(admin))
            adminEmail = admin[irand][0]
            today = datetime.datetime.now().date()
            category = request.POST["category"].lower()
            link = request.POST["link"]
            cursor.execute("select id from kategori_pd where nama_kategori=%s",[category])
            categoryID = cursor.fetchall()[0][0]
            cursor.execute(f"insert into penggalangan_dana_pd values('{id}','{judul}','{deskripsi}','{kota}','{provinsi}','{link}','Belum verifikasi',CAST('{today}' AS DATE),null,CAST('{deadline}' AS DATE),{target},null,null,null,'{email}','{adminEmail}','{categoryID}')")
            if category == "kesehatan":
                nik = request.POST["NIK"]
                penyakit = request.POST["penyakit"]
                cursor.execute(f"insert into pd_kesehatan values('{id}','{penyakit}','{nik}')")
            elif category == "rumah ibadah":
                noSertif = request.POST["noSertif"]
                aktivitas = request.POST["select"]
                cursor.execute(f"select id from kategori_aktivitas_pd_rumah_ibadah where nama='{aktivitas}'")
                idaktiv = cursor.fetchall()[0][0]
                cursor.execute(f"insert into pd_rumah_ibadah values('{id}','{noSertif}','{idaktiv}')")
            
            return redirect("penggalangan_dana:daftar_PD")
    return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)


def komorbid(request):
    with connection.cursor() as cursor:
        cursor.execute("select K.idPD, PD.judul, Kes.penyakit, K.komorbid from sidona.komorbid K left join sidona.penggalangan_dana_pd PD on PD.id = K.idPD left join sidona.PD_Kesehatan Kes on K.idPD = Kes.idPD")
        komorbid = cursor.fetchall()
        response = {
            'komorbid': komorbid,
        }
    return render(request, "penggalangan/Komorbid/komorbid.html", response)


def komorbid_tambah(request):
    with connection.cursor() as cursor:
        cursor.execute("select Kes.idPD from sidona.PD_Kesehatan Kes")
        idPD = cursor.fetchall()
        response = {
            'idPD': idPD,
        }
        if request.method == "POST":
            id = request.POST["select"]
            penyakit = request.POST["penyakit"]
            cursor.execute("insert into sidona.komorbid values (%s,%s)", [id,penyakit])
            return redirect("penggalangan_dana:komorbid")
    return render(request, "penggalangan/Komorbid/form_tambah.html", response)

def komorbid_update(request,id):
    with connection.cursor() as cursor:
        cursor.execute("select K.idPD, K.komorbid from sidona.komorbid K left join sidona.penggalangan_dana_pd PD on PD.id = K.idPD where K.idPD = %s", [id])
        komorbid = cursor.fetchall()
        response = {
            'komorbid': komorbid,
        }
        if request.method == "POST":
            komorbid = request.POST["penyakit"]
            cursor.execute("update sidona.komorbid set komorbid=%s where idPD = %s",[komorbid,id])
            return redirect("penggalangan_dana:komorbid")
    return render(request, "penggalangan/Komorbid/form_update.html",response)
