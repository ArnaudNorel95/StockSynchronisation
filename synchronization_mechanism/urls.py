from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from stock import forms
from datetime import datetime
from . import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('logout/',
        LogoutView.as_view(
            next_page='/'
        ),
        name='logout'
    ),

    path('password_change/',
        PasswordChangeView.as_view(),
        name='password_change'
    ),

    path('password_change_done/',
        PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),

    path('password_reset/',
        PasswordResetView.as_view(),
        name='password_reset'
    ),

    path('password_reset_done/',
        PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    path('password_reset_confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path('password_reset_complete/',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

    # path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls, name="admin"),
    path('', include('stock.urls', namespace='stock')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
