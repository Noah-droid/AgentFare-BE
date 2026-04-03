from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorldViewSet, ResourceNodeViewSet

router = DefaultRouter()
router.register(r'', WorldViewSet)
router.register(r'resources', ResourceNodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
