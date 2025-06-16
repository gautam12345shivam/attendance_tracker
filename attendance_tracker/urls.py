from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # ✅ Import this
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Attendance App URLs
    path('', include('attendance.urls')),

    # Home page
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
]
