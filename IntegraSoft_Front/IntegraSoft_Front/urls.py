"""IntegraSoft_Front URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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



urlpatterns = [
    path('admin/', admin.site.urls),
    path('works/', include('mantenedor_works.urls') ), 
    path("cuenta/", include('cuenta.urls')),
    path('novedades/', include('novedades.urls')), 
    path('', include('templates_generales.urls') ),
   
]


#ignore: llamamos a IndewsView desde nuestra app "templates_generales" debido a que no tenemos
#views como tal en nuestra app de configuracion, después de llamar a las views de nuestra app podemos 
#utilizar el login_required, solucionamos el problema de logout que redirigia al admin con un "next page"
