from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'items', views.RegistryViewSet)

from . import views

urlpatterns = [
    path('', include(router.urls)),
    path('claim/', views.claim, name="claim"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]