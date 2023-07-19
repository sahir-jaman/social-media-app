from django.contrib import admin
from django.urls import path, include
from users_app import views

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Authentication app Urls:
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth", include("authentication.urls")),
    path("api/v1/user", include("users_app.urls")),
    path('api/v1', include('post_app.urls')),

    # # YOUR PATTERNS
    path('', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
]
