from django.db import models
from django.contrib.auth.models import User
from django.conf import settings # Use settings.AUTH_USER_MODEL for ForeignKey
from metroline.models import Station 
import uuid 

# --- Wallet Model ---
class Wallet(models.Model):
    # One-to-one relationship with the user ensures each user has only one wallet
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='passenger_wallet') 
    # Max digits 10, decimal places 2 (e.g., 9,999,999,999.99)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet for {self.user.username} (Balance: {self.balance})"

# --- Ticket Model ---
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'), # Just purchased, ready for entry
        ('In Use', 'In Use'), # Entered the station, waiting for exit scan
        ('Used', 'Used'),     # Exited the station
        ('Expired', 'Expired'),
    ]
    
    # Use UUID for easy scanning/input
    ticket_id = models.UUIDField(default=uuid.uuid4, unique=True)
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # PROTECT prevents a Station from being deleted if a ticket refers to it
    start_station = models.ForeignKey(Station, related_name='starting_tickets', on_delete=models.PROTECT)
    end_station = models.ForeignKey(Station, related_name='ending_tickets', on_delete=models.PROTECT)
    
    price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    
    purchase_time = models.DateTimeField(auto_now_add=True)
    entry_scan_time = models.DateTimeField(null=True, blank=True)
    exit_scan_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.ticket_id.hex[:6]} - {self.start_station} to {self.end_station}"