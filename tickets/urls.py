from django.urls import path
from . import views

urlpatterns = [
    # Wallet Management Views
    path('wallet/', views.wallet_view, name='wallet_view'),
    path('add_funds/', views.add_funds, name='add_funds'),
    
    # Ticket Purchasing Views
    path('buy/', views.buy_ticket, name='buy_ticket'),
    
    # Ticket History Views
    path('history/', views.ticket_history, name='ticket_history'),
]