"""SystemGraph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static

from . import common_views

about_patterns = [
	path('', common_views.about_SystemGraph, name='about'),
]

tutorial_patterns = [
	path('', common_views.tutorial_frontpage, name='tutorial_frontpage'),
	path('register/', common_views.tutorial_register, name='tutorial_register'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
	path('users/', include('users.urls')),
	path('profile/', include('userprofile.urls')),
    path('graph/', include('SGMain.urls')),
    path('ajax/', include('SGMain.ajax_urls')),
    path('', common_views.frontpage, name='start'),
	
	path('about/', include(about_patterns)),
	
	path('tutorial/', include(tutorial_patterns)),
]

from django.conf import settings
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)