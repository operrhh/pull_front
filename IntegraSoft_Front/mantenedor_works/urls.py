# from django.urls import path
# from django.contrib.auth.decorators import login_required
# from . import views

# urlpatterns = [
#     path('', login_required (views.index), name="index_mantenedor_usuarios"),
#     path('usuarios', views.Persona, name="usuarios_mantenedor_works"),
#     path('buscar_usuarios', views.buscar_usuarios, name="buscar_usuarios_mantenedor_works"),
#     path('obtener_opciones_por_base/', views.obtener_opciones_por_base, name='obtener_opciones_por_base_mantenedor_works'),
#     path('works/buscar_usuarios/detalles/<str:base_datos>/<str:user_id>/', views.detalles_usuario, name='detalles_usuario_mantenedor_works')


# ]
# #los works ya están clutcheados por parte del login_Required

from django.urls import path
from . import views

app_name = 'workers' 

urlpatterns = [
    path('', views.index, name="index_mantenedor_usuarios"),  # Quita login_required
    path('buscar_usuarios', views.buscar_usuarios, name="buscar_usuarios_mantenedor_works"),
   ]


