"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

admin.site.site_header = 'INKA Backend'                   # default: "Django Administration"
admin.site.index_title = 'Administración del sitio'                 # default: "Site administration"

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('admin/', admin.site.urls),
    path('security/', include('security.urls')),
    path('product/', include('product.urls')),
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),
]
