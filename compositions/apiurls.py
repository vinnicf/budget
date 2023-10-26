from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CompositionViewSet, SearchCompositionView, CompositionDetailView, CompositionCostView
from . import views_excel

router = DefaultRouter()
router.register(r'compositions', CompositionViewSet)

urlpatterns = router.urls + [
    path('search-compositions/', SearchCompositionView.as_view(), name='search_compositions'),
    path('composition/<str:codigo>/', CompositionDetailView.as_view(), name='composition_detail'),
    path('composition/<str:codigo>/<str:state>/<str:desonerado>/', CompositionCostView.as_view(), name='composition_cost'),
    path('export_excel/', views_excel.export_excel, name='export_excel')
]