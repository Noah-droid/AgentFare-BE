from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/worlds/', include('worlds.urls')),
    path('api/agents/', include('agents.urls')),
    path('api/economy/', include('economy.urls')),
    path('api/events/', include('events.urls')),
]
