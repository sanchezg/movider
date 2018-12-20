"""movider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from providers import views, viewsets

router = routers.DefaultRouter()
router.register(r'currencies', viewsets.CurrencyViewSet)
router.register(r'providers', viewsets.ProviderViewSet)
router.register(r'serviceareas', viewsets.ServiceAreaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v0/', include(router.urls)),
    url(r'^api/v0/servicesareas_by_location/$',
        views.ServiceAreasList.as_view(),
        name="servicesareas_by_location"),
]
