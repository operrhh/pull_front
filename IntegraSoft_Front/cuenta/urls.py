from django.urls import path
from . import views

app_name = 'cuenta'

urlpatterns = [
    path('', views.index, name="index_cuenta"),
]

#la ruta para cuenta está clutch
