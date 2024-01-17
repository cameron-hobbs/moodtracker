from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from patient.urls import patient_router
from moodtracker import views
from moodtracker.admin import admin_site
from moodtracker.views import SmsWebhook

urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/sms_webhook/', SmsWebhook.as_view()),
    path('api/auth/token/', TokenObtainPairView.as_view(), name="access_token"),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name="refresh_token"),
    path('api/mood_tracker/', include(patient_router.urls))
]

if settings.ENVIRONMENT != "local":
    urlpatterns = urlpatterns + [re_path(".*", views.index, name="index")]
else:
    urlpatterns = urlpatterns + [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
    ]

# figure out if this only needed locally too
urlpatterns = urlpatterns + static("static/", document_root="/app/static/")
