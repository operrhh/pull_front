from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import IndexView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='templates_generales/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', login_required (IndexView.as_view()), name="index_home"),
    # Otras URLs 
]