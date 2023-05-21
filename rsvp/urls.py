from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'invites', views.InviteViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('rsvp/', views.submit_rsvp),
    path('send-emails/', views.send_emails),
    path('test-email/', views.test_email),
    path('dry-run/', views.dry_run),
    path('send-specific/', views.send_specific),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('export/', views.generate_xlsx_spreadsheet)
]
