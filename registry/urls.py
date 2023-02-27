from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'items', views.RegistryViewSet)
router.register(r'funds', views.FundViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('claim/', views.claim, name="claim"),
    path('contribute/', views.contribute, name="contribute"),
    path('contribution-amount/', views.get_contribution_amount),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
