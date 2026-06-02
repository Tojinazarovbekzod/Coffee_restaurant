from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.crm_dashboard, name='dashboard'),
    path('mijozlar/', views.mijozlar_royxati, name='mijozlar'),
    path('mijozlar/yangi/', views.mijoz_yaratish, name='mijoz_yaratish'),
    path('mijozlar/<int:pk>/', views.mijoz_detail, name='mijoz_detail'),
    path('mijozlar/<int:pk>/tahrirlash/', views.mijoz_tahrirlash, name='mijoz_tahrirlash'),
    path('mijozlar/<int:pk>/ochirish/', views.mijoz_ochirish, name='mijoz_ochirish'),
    path('mijozlar/<int:mijoz_pk>/muloqot/', views.muloqot_qoshish, name='muloqot_qoshish'),
]
