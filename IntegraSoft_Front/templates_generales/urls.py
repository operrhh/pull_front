from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import IndexView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='templates_generales/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', IndexView.as_view(), name="index_home"),
    # Otras URLs 
]