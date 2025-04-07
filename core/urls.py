"""
URL configuration for core project.

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
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('library/', include('library.urls')),
    path('library/<version>/', include('library.urls')),
    path('library/v1/schema/', SpectacularAPIView.as_view(api_version='v1'), name='schema-v1'),
    path('library/v2/schema/', SpectacularAPIView.as_view(api_version='v2'), name='schema-v2'),
    path('library/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema-v1'), name='swagger-ui-v1'),
    path('library/v2/docs/', SpectacularSwaggerView.as_view(url_name='schema-v2'), name='swagger-ui-v2'),
]
