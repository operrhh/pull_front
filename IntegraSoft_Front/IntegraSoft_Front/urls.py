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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import  LoginView
from django.contrib.auth.views import LogoutView
from templates_generales.views import IndexView


app_name = 'templates_generales'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('works/', include('mantenedor_works.urls') ), 
    path("cuenta/", include('cuenta.urls')),
    path('', login_required(IndexView.as_view()), name="index_home"),
    path('accounts/login/', LoginView.as_view(template_name='templates_generales/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]


#ignore: llamamos a IndewsView desde nuestra app "templates_generales" debido a que no tenemos
#views como tal en nuestra app de configuracion, después de llamar a las views de nuestra app podemos 
#utilizar el login_required, solucionamos el problema de logout que redirigia al admin con un "next page"
