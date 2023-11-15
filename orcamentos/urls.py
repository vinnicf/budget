from rest_framework.routers import DefaultRouter
from .views import OrcamentoViewSet, OrcamentoItemViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'orcamentos', OrcamentoViewSet)
router.register(r'orcamento_items', OrcamentoItemViewSet)

urlpatterns = [
    # ... your other url patterns ...
    path('', include(router.urls)),
]
