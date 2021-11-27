from django.db import models
# from django.core.validators import 

# Create your models here.
# class Pengguna(models.Model):
#     Email = models.CharField(max_length=255)
#     Nama = models.CharField(max_length=255)
#     NomorHp = models.IntegerField(max_length=12)
#     Alamat = models.CharField(max_length=255)
#     NamaBank = models.CharField(max_length=10)
#     NoRekening = models.IntegerField(max_length=20)
#     SaldoDonaPay = models.DecimalField(max_digits=8, decimal_places=2)
#     # Jenis
    
#     class Organisasi(models.Model):
#         NamaOrganisasi = models.CharField(max_length=255)
#         NomorAkta = models.CharField(max_length=255)
#         NoTelp = models.IntegerField(max_length=12)
#         TahunBerdiri = models.IntegerField(max_length=4)
#         FotoAkta = models.ImageField(null = True, blank = True)
        
        
#     class Individu(models.Model):
#         NIK = models.IntegerField(max_length=16)
#         TanggalLahir = models.DateField(auto_now_add=True, auto_now=True, blank=True)
#         jenisKelamin_choices = (
#             ('Laki-laki', 'Laki-laki')
#             ('Perempuan', 'Perempuan')
#         )
#         JenisKelamin = models.CharField(max_length=10, blank=True, null=True, choices=jenisKelamin_choices)
#         FotoKtp = models.ImageField(null = True, blank = True)
        