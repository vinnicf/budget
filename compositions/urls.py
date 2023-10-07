from django.urls import path
from . import views


app_name = 'compositions'

urlpatterns = [
    path('composition/<str:codigo>/', views.composition_detail, name='composition_detail'),
    path('insumo/<str:codigo>/', views.insumo_detail, name='insumo_detail'),
    path('list/', views.composition_list, name='composition_list'),
]
