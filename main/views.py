from django.http import response
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.db import connection



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
    if(request.session.get("username")!=None):
        return redirect("main:home")
    if request.method == "POST":
        with connection.cursor() as cursor:
            email = request.POST["email"]
            password = request.POST["password"]
            # ini buat execute query database
            cursor.execute("select * from admin where email=%s and password=%s",[email,password])

            row = cursor.fetchall() # ini dibalikin dalem bentuk multi-dimensional array
            if (len(row) != 0): # Berhasil login
                print("test")
                # contohnya buat set session.username menjadi row pertama (index ke 0) kolom pertama (index ke 0)
                # dalem kasus gw, kolom username adalah kolom paling awal di table PENGGUNA
                request.session["username"] = row[0][0] 
                request.session["password"] = row[0][1] 
                request.session["peran"] = "admin"
                return redirect("main:home")
            else:
                cursor.execute("select * from penggalang_dana where email=%s and password=%s",[email,password])
                row = cursor.fetchall()
                if (len(row) != 0): # Berhasil login

                        # contohnya buat set session.username menjadi row pertama (index ke 0) kolom pertama (index ke 0)
                        # dalem kasus gw, kolom username adalah kolom paling awal di table PENGGUNA
                        request.session["username"] = row[0][0] 
                        request.session["password"] = row[0][1] 
                        request.session["peran"] = "penggalang_dana"
                        return redirect("main:home")
                
                else: # Gagal login
                    messages.add_message(request, messages.WARNING, "Maaf, username atau password salah.")

    return render(request, "login/login.html")

def register(request):
    return render(request, "login/register.html")

def increment_id_admin():
    with connection.cursor() as cursor:
        cursor.execute("select id_pegawai from admin order by id_pegawai desc limit 1")
        newID = cursor.fetchall()
        newID= str(int(newID[0][0])+1)
    return newID
def register_admin(request):
    if request.session.get("username", False):
        return redirect("main:home")

    if request.method == "POST":
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""select * from admin WHERE username = '{request.POST["username"]}'""")

                if (len(cursor.fetchall()) == 0):
                    id_pegawai = increment_id_admin()
                    cursor.execute(f"""
                        INSERT INTO admin VALUES
                        ('{request.POST["username"]}', '{request.POST["password"]}', '{request.POST["nama"]}','{request.POST["noHP"]}','{id_pegawai}')
                    """)
                    messages.add_message(request, messages.SUCCESS, f"Registrasi berhasil, silahkan login")
                    messages.add_message(request, messages.SUCCESS, f"{request.POST['username']}")
                    return render(request, "authentication/register.html")
            
            # Ada username yang sama, handle disini
            except IntegrityError:
                messages.add_message(request, messages.WARNING, f"Username {request.POST['username']} sudah ada")
            except:
                traceback.print_exc()
                print(request.POST.get("kode", False))
                messages.add_message(request, messages.WARNING, f"Ada gangguan server internal, mohon coba lagi")
    return render(request, "login/register_admin.html")

def register_user(request):
    
    
    
    
    return render(request, "login/register_user.html")

def register_user_individu(request):
    return render(request, "login/individu.html")

def register_user_organisasi(request):
    return render(request, "login/organisasi.html")

def list_pengguna_terdaftar(request):
    return render(request, "admin/list_pengguna.html")

def logout(request):
    if "username" in request.session:
        request.session.flush()
        return redirect('/login')
    return redirect('login/register.html')
