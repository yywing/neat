"""neat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from raw.urls import router as raw_router
from normal.urls import router as normal_router
from utils.rest.routers import DefaultRouter

# router
router = DefaultRouter()
router.extend(raw_router)
router.extend(normal_router)


# swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="NEAT API",
        default_version='v1',
        description="Save HTTP flow and make website structure clear.",
        terms_of_service="https://github.com/yywing/neat",
    ),
    public=True,
)
schema_url = [
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns = [
    *schema_url,
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
