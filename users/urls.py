from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Custom login view using Django's built-in form and our custom login.html template
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # The home page after login
    path('', views.home, name='home'), 
]