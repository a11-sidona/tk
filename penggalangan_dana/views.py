from django.http import response, JsonResponse
from django.shortcuts import render, redirect
from django.db import connection
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
        cursor.execute("select pd.id, pd.judul, pd.kota, pd.provinsi, pd.tanggal_aktif_awal, pd.tanggal_aktif_akhir, pd.sisa_hari, pd.jumlah_dibutuhkan, k.nama_kategori, pd.status_verifikasi, p.jumlah_pd, p.jumlah_pd_aktif from penggalangan_dana_pd pd, penggalang_dana p, kategori_pd k where pd.email_user = p.email and pd.id_kategori=k.id and pd.email_user = %s",[request.session.get("username")])
        result = namedtuple_fetch_all(cursor)
        response ={
            "hasil":result
        }
    return render(request, "penggalangan/admin/daftar_PD_pribadi.html", response)


def form_update(request):
    kategori = request.GET.get("kategori", "lainnya")
    response = {"kategori": kategori}
    return render(request, "penggalangan/form_update.html", response)


def form_verifikasi(request):
    return render(request, "penggalangan/form_verifikasi.html")


def form_tambah_kategori(request):
    return render(request, "penggalangan/kategori/form_tambah.html")


def list_kategori(request):
    return render(request, "penggalangan/kategori/list.html")


def form_update_kategori(request):
    return render(request, "penggalangan/kategori/form_update.html")


def detail_penggalangan(request):
    id = request.GET.get("id", "1")
    response = {"id": id}
    return render(request, "penggalangan/detail_penggalangan.html", response)


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
            response["category"] = category
            return render(
                request, "penggalangan/create_PD/form_penggalangan_dana.html", response
            )

    return render(request, "penggalangan/create_PD/form_kategori.html", response)


def increment_id_pd():
    with connection.cursor() as cursor:
        cursor.execute("select id from sidona.penggalangan_dana_pd order by id desc limit 1")
        newID = cursor.fetchall()
        newID= str(int(newID[0][0])+1)
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
            cursor.execute("select nama from sidona.pasien where nik = %s", [nik])
            response["category"] = "Kesehatan"
            response["NIK"] = nik
            response["nama"] = cursor.fetchall()
            response["id"] = increment_id_pd()
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
            response["category"] = "Rumah Ibadah"
            response["noSertif"] = noSertif
            cursor.execute("select nama from sidona.kategori_aktivitas_pd_rumah_ibadah")
            response["kategori"] = cursor.fetchall()
            response["id"] = increment_id_pd()
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
            response["category"] = "Kesehatan"
            response["NIK"] = nik
            response["nama"] = cursor.fetchall()
            response["id"] = increment_id_pd()
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
            response["category"] = "Rumah Ibadah"
            response["noSertif"] = noSertif
            cursor.execute("select nama from sidona.kategori_aktivitas_pd_rumah_ibadah")
            response["kategori"] = cursor.fetchall
            cursor.execute("insert into rumah_ibadah values (%s,%s,%s,%s)",[noSertif, nama, alamat, jenis])
            response["id"] = increment_id_pd()
            return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/form_rumah_ibadah.html")


def form_PD(request):
    with connection.cursor() as cursor:
        response = {}
        response["id"] = increment_id_pd()
        if request.method == "POST":
            category = request.POST["category"]
            if category == "Kesehatan":
                nik = request.POST["NIK"]
                response = {}
                response["category"] = "Kesehatan"
                response["NIK"] = nik
                return render(
                    request, "penggalangan/admin/daftar_PD_pribadi.html", response
                )
            elif category == "Rumah Ibadah":
                noSertif = request.POST["noSertif"]
                response = {}
                response["category"] = "Rumah Ibadah"
                response["noSertif"] = noSertif
                return render(
                    request, "penggalangan/admin/daftar_PD_pribadi.html", response
                )
            else:
                response = {}
                response["category"] = category
                return render(request, "penggalangan/admin/daftar_PD_pribadi.html", response)
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
