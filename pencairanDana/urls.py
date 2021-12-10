from django.urls import path, include
from .views import *

urlpatterns = [
    path('profile',index , name='index'),
    path('formPencairan', pencairanDana, name='pencairanDana'),
    path("detailPenggalangan", detailPenggalangan, name="detailPenggalangan"),
    path('formPencairan2', cairDana, name='cairDana'),
]
