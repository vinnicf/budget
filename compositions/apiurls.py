from rest_framework.routers import DefaultRouter
from .views import CompositionViewSet

router = DefaultRouter()
router.register(r'compositions', CompositionViewSet)

urlpatterns = router.urls
