from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorldEventViewSet

router = DefaultRouter()
router.register(r'', WorldEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
