from django.urls import path, include
from .views import *


# app_name = 'pencairan'

urlpatterns = [
    path('profile',index , name='index'),
    path('formPencairan', pencairanDana, name='pencairanDana'),
    # path('detailPenggalangan/<str:kode>', detailPenggalangan, name="detailPenggalangan"),
    path('detailPenggalangan', detailPenggalangan, name='detailPenggalangan'),
    path('formPencairan2', cairDana, name='cairDana'),
]
