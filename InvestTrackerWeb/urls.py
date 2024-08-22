"""
URL configuration for InvestTrackerWeb project.

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

# Importar views:
from coreApp import views as coreViews
from assets import views as assetsViews
from accounts import views as accViews

urlpatterns = [
    # ADMIN, CORE, HOME
    path('admin/', admin.site.urls),
    path('', coreViews.home,name='home'),


    # ASSETS
    path('configure/', assetsViews.configureAssets,name='configure'),
    path('check/', assetsViews.checkAssets,name='check'),
    path('search/', assetsViews.searchAssets,name='search'),


    # ACCOUNT MANAGER
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', accViews.register, name='register'),

]
