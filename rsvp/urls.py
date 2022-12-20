from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'invites', views.InviteViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('rsvp/', views.submit_rsvp),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
