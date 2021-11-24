from django.shortcuts import render


def daftar_penggalangan(request):
    return render(request, "penggalangan/daftar_penggalangan.html")


def daftar_penggalangan_admin(request):
    return render(request, "penggalangan/admin/daftar_penggalangan.html")

def form_update(request):
    return render(request, "penggalangan/form_update.html")

def create_PD_category(request):
    if request.method == "POST":
        category = request.POST["category"]

        response = {}
        response["category"] = category
        return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/form_kategori.html")

def cek_pasien(request):
    if request.method == "POST":
        nik = request.POST["NIK"]
        response = {}
        response["category"] = "Kesehatan"
        response["NIK"] = nik
        return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/cek_pasien.html")

def cek_rumah(request):
    if request.method == "POST":
        noSertif = request.POST["noSertif"]

        response = {}
        response["category"] = "Rumah Ibadah"
        response["noSertif"] = noSertif
        return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/cek_rumah_ibadah.html")

def daftar_pasien(request):
    if request.method == "POST":
        nik = request.POST["NIK"]

        response = {}
        response["category"] = "Kesehatan"
        response["NIK"] = nik
        return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/form_pasien.html")

def daftar_rumah(request):
    if request.method == "POST":
        noSertif = request.POST["noSertif"]

        response = {}
        response["category"] = "Rumah Ibadah"
        response["noSertif"] = noSertif
        return render(request, "penggalangan/create_PD/form_penggalangan_dana.html", response)

    return render(request, "penggalangan/create_PD/form_rumah_ibadah.html")

def form_PD(request):
    if request.method == "POST":
        category = request.POST["category"]
        if(category == "Kesehatan"):
            nik = request.POST["NIK"]
            response = {}
            response["category"] = "Kesehatan"
            response["NIK"] = nik
            return render(request, "penggalangan/admin/daftar_penggalangan.html", response)
        elif(category == "Rumah Ibadah"):
            noSertif = request.POST["noSertif"]
            response = {}
            response["category"] = "Rumah Ibadah"
            response["noSertif"] = noSertif
            return render(request, "penggalangan/admin/daftar_penggalangan.html", response)
        else:
            response = {}
            response["category"] = category
            return render(request, "penggalangan/admin/daftar_penggalangan.html", response)
    return render(request, "penggalangan/create_PD/form_penggalangan_dana.html")