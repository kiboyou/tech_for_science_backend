"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from user.views import GroupViewSet

router = routers.DefaultRouter()


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="BACKEND TECH FOR SCIENCE",

   ),
   public=True,
   permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    # Home page: nice welcome screen for the Admin site
    path(
        "",
        TemplateView.as_view(template_name="admin_welcome.html"),
        name="home",
    ),
    path("admin/", admin.site.urls),
    # Django i18n: provides the built-in 'set_language' view used by language choosers
    path('i18n/', include('django.conf.urls.i18n')),
    
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/groupe/', GroupViewSet.as_view({'get': 'list', 'post': 'create'}), name="groupeUtilisateur"),
    path('api/groupe/<int:pk>/', GroupViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="groupeUtilisateur-detail"),
    
    path('api/user/', include('user.urls')),
    path('api/main/', include('main.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]