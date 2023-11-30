from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CompositionViewSet, SearchCompositionView, CompositionDetailView, CompositionCostView, SearchInsumoView, InsumoCostView
from . import views_excel

router = DefaultRouter()
router.register(r'compositions', CompositionViewSet)

urlpatterns = router.urls + [
    path('search-compositions/', SearchCompositionView.as_view(), name='search_compositions'),
    path('search-insumos/', SearchInsumoView.as_view(), name='search-insumo'),
    path('composition/<str:codigo>/', CompositionDetailView.as_view(), name='composition_detail'),
    path('composition/<str:codigo>/<str:state_name>/<str:desonerado>/<str:year_month>/', CompositionCostView.as_view(), name='composition_cost'),
    path('insumo/<str:codigo>/<str:state_name>/<str:desonerado>/', InsumoCostView.as_view(), name='insumo_cost'),
    path('export_excel/', views_excel.export_excel, name='export_excel')
]