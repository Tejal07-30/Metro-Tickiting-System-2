from django.urls import path
from . import views

urlpatterns = [
    # The main interface for scanning tickets
    path('scan/', views.scanner_interface, name='scanner_interface'),
    # Endpoint to handle the actual ticket scan (entry/exit)
    path('scan_ticket/', views.scan_ticket, name='scan_ticket'),
    # Interface for creating offline tickets
    path('offline_purchase/', views.offline_purchase, name='offline_purchase'),
]