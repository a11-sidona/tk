from django.urls import path
from donasi.views import detail_donasi, form_donasi, index

urlpatterns = [
    path('', index, name='dataDonasi'),
    path('form-donasi', form_donasi, name='formDonasi'),
    path('detail-donasi', detail_donasi, name='detailDonasi')
]