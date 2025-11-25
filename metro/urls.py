from django.contrib import admin
from django.urls import path, include  

urlpatterns = [
    path('admin/', admin.site.urls),
    # Built-in Auth URLs (handles login/logout using our templates)
    path('', include('django.contrib.auth.urls')), 
    
    # Links to the custom URLs in the 'users' app
    path('', include('users.urls')), 
    
    # LINKS TO THE SCANNER APP:
    path('scanner/', include('scanner.urls')),
    # LINKS TO THE TICKETS APP:
    path('tickets/', include('tickets.urls')), 
    
]
