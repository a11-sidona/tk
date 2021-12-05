from django.shortcuts import render
from django.db import connection
from penggalangan_dana.utils import namedtuple_fetch_all


def daftar_penggalangan(request):
    return render(request, "penggalangan/daftar_penggalangan.html")


def daftar_penggalangan_admin(request):
    cursor_p = connection.cursor()
    query = """
            SELECT pd.id, judul, kota, provinsi, tanggal_aktif_awal, tanggal_aktif_akhir, sisa_hari, jumlah_dibutuhkan, nama_kategori, status_verifikasi
            FROM sidona.penggalangan_dana_pd pd, sidona.kategori_pd k
            WHERE pd.id_kategori = k.id;
            """
    cursor_p.execute(query)
    pds = namedtuple_fetch_all(cursor_p)
    return render(
        request, "penggalangan/admin/daftar_penggalangan.html", {"pds": pds}
    )


def daftar_penggalangan_PD(request):
    return render(request, "penggalangan/admin/daftar_PD_pribadi.html")


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
    if request.method == "POST":
        category = request.POST["category"]

        response = {}
        response["category"] = category
        return render(
            request, "penggalangan/create_PD/form_penggalangan_dana.html", response
        )

    return render(request, "penggalangan/create_PD/form_kategori.html")


def cek_pasien(request):
    if request.method == "POST":
        nik = request.POST["NIK"]
        response = {}
        response["category"] = "Kesehatan"
        response["NIK"] = nik
        return render(
            request, "penggalangan/create_PD/form_penggalangan_dana.html", response
        )

    return render(request, "penggalangan/create_PD/cek_pasien.html")


def cek_rumah(request):
    if request.method == "POST":
        noSertif = request.POST["noSertif"]

        response = {}
        response["category"] = "Rumah Ibadah"
        response["noSertif"] = noSertif
        return render(
            request, "penggalangan/create_PD/form_penggalangan_dana.html", response
        )

    return render(request, "penggalangan/create_PD/cek_rumah_ibadah.html")


def daftar_pasien(request):
    if request.method == "POST":
        nik = request.POST["NIK"]

        response = {}
        response["category"] = "Kesehatan"
        response["NIK"] = nik
        return render(
            request, "penggalangan/create_PD/form_penggalangan_dana.html", response
        )

    return render(request, "penggalangan/create_PD/form_pasien.html")


def daftar_rumah(request):
    if request.method == "POST":
        noSertif = request.POST["noSertif"]

        response = {}
        response["category"] = "Rumah Ibadah"
        response["noSertif"] = noSertif
        return render(
            request, "penggalangan/create_PD/form_penggalangan_dana.html", response
        )

    return render(request, "penggalangan/create_PD/form_rumah_ibadah.html")


def form_PD(request):
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
            return render(
                request, "penggalangan/admin/daftar_PD_pribadi.html", response
            )
    return render(request, "penggalangan/create_PD/form_penggalangan_dana.html")


def komorbid(request):
    return render(request, "penggalangan/Komorbid/komorbid.html")


def komorbid_tambah(request):
    if request.method == "POST":
        return render(request, "penggalangan/Komorbid/komorbid.html")
    return render(request, "penggalangan/Komorbid/form_tambah.html")


def komorbid_update(request):
    if request.method == "POST":
        return render(request, "penggalangan/Komorbid/komorbid.html")
    return render(request, "penggalangan/Komorbid/form_update.html")
