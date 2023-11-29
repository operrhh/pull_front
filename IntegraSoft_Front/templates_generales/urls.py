from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import IndexView, login_view
urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', IndexView.as_view(), name="index_home"),
    # Otras URLs 
]