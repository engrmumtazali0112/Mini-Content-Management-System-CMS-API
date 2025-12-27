from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView
from django.http import JsonResponse

# Simple homepage view
def api_root(request):
    return JsonResponse({
        'message': 'Welcome to Mini CMS API',
        'version': 'v1',
        'endpoints': {
            'api_documentation': request.build_absolute_uri('/swagger/'),
            'admin_panel': request.build_absolute_uri('/admin/'),
            'authentication': request.build_absolute_uri('/api/auth/'),
            'articles': request.build_absolute_uri('/api/articles/'),
            'categories': request.build_absolute_uri('/api/categories/'),
            'scraper': request.build_absolute_uri('/api/scraper/'),
        }
    })

schema_view = get_schema_view(
    openapi.Info(
        title="Mini CMS API",
        default_version='v1',
        description="A comprehensive Content Management System API with JWT authentication",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@minicms.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Homepage - Add this line
    path('', api_root, name='api-root'),
    
    path('admin-panal/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('accounts.urls')),
    path('api/', include('articles.urls')),
    path('api/scraper/', include('scraper.urls')),
    
    # Swagger/OpenAPI documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)