from django.urls import path
from .views import login_view, home_view, logout_view

app_name = 'accounts'

urlpatterns = [
    path('home/', home_view, name='index_home'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # Otras URLs
]
