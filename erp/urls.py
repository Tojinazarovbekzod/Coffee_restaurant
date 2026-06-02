from django.urls import path
from . import views

app_name = 'erp'

urlpatterns = [
    path('', views.erp_dashboard, name='dashboard'),
    path('mahsulotlar/', views.mahsulotlar, name='mahsulotlar'),
    path('mahsulotlar/yangi/', views.mahsulot_yaratish, name='mahsulot_yaratish'),
    path('mahsulotlar/<int:pk>/tahrirlash/', views.mahsulot_tahrirlash, name='mahsulot_tahrirlash'),
    path('mahsulotlar/<int:pk>/ochirish/', views.mahsulot_ochirish, name='mahsulot_ochirish'),
    path('buyurtmalar/', views.buyurtmalar, name='buyurtmalar'),
    path('buyurtmalar/yangi/', views.buyurtma_yaratish, name='buyurtma_yaratish'),
    path('buyurtmalar/<int:pk>/', views.buyurtma_detail, name='buyurtma_detail'),
    path('buyurtmalar/<int:pk>/holat/', views.buyurtma_holat, name='buyurtma_holat'),
    path('xodimlar/', views.xodimlar, name='xodimlar'),
    path('xodimlar/yangi/', views.xodim_yaratish, name='xodim_yaratish'),
    path('xodimlar/<int:pk>/tahrirlash/', views.xodim_tahrirlash, name='xodim_tahrirlash'),
    path('moliya/', views.moliya, name='moliya'),
    path('moliya/yangi/', views.moliya_qoshish, name='moliya_qoshish'),
]
