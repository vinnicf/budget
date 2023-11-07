from django.urls import path
from . import views


app_name = 'compositions'

urlpatterns = [
    path('composicao/<str:codigo>/', views.composition_detail, name='composition_detail'),
    path('compositions/pesquisa/', views.composition_search_view, name='composition_search'),
    path('insumo/<str:codigo>/', views.insumo_detail, name='insumo_detail'),
    path('insumos/', views.insumo_list_view, name='insumo_list'),
    path('sinapi/', views.classes_list, name='classes_list'),
    path('classe/<str:code>/', views.classe_detail, name='classe_detail'),
    path('grupo/<int:grupo_id>/', views.grupo_detail, name='grupo_detail'),
    path('list/', views.composition_list, name='composition_list'),
    path('', views.home_view, name='home'),
]
