from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
import uuid

# We need these models:
from metroline.models import Station
from tickets.models import Wallet, Ticket

# --- HELPER FUNCTIONS ---

def calculate_ticket_price(start_station, end_station):
    """Placeholder for a real price calculation based on distance/zones."""
    
    # Simplified logic: 
    # If the station names are different, the price is 10.00. If same (testing), 0.00.
    if start_station.name != end_station.name:
        return 10.00
    return 0.00 

def get_or_create_wallet(user):
    """Ensures every passenger user has an associated wallet."""
    wallet, created = Wallet.objects.get_or_create(user=user, defaults={'balance': 0.00})
    return wallet

# --- WALLET VIEWS ---

@login_required
def wallet_view(request):
    """Displays the passenger's current wallet balance."""
    wallet = get_or_create_wallet(request.user)
    return render(request, 'tickets/wallet_view.html', {'wallet': wallet})

@login_required
@transaction.atomic
def add_funds(request):
    """Handles adding funds (e.g., simulating a transaction) to the wallet."""
    wallet = get_or_create_wallet(request.user)

    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            if amount > 0:
                wallet.balance += amount
                wallet.save()
                messages.success(request, f"Successfully added ₹{amount:.2f} to your wallet.")
                return redirect('wallet_view')
            else:
                messages.error(request, "Amount must be greater than zero.")
        except ValueError:
            messages.error(request, "Invalid amount entered.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    # For GET requests or failed POST requests, render the form
    return render(request, 'tickets/add_funds.html', {'wallet': wallet})

# --- TICKET VIEWS ---

@login_required
@transaction.atomic
def buy_ticket(request):
    """Allows passenger to purchase a single-ride ticket."""
    wallet = get_or_create_wallet(request.user)
    stations = Station.objects.all().order_by('name')

    if request.method == 'POST':
        start_station_id = request.POST.get('start_station')
        end_station_id = request.POST.get('end_station')
        
        try:
            start_station = get_object_or_404(Station, id=start_station_id)
            end_station = get_object_or_404(Station, id=end_station_id)
            
            price = calculate_ticket_price(start_station, end_station)

            if wallet.balance >= price:
                # 1. Deduct cost from wallet
                wallet.balance -= price
                wallet.save()

                # 2. Create the new ticket (Active status)
                Ticket.objects.create(
                    passenger=request.user,
                    start_station=start_station,
                    end_station=end_station,
                    price=price,
                    status='Active', # Ready for use
                    ticket_id=uuid.uuid4() # Generate a unique UUID for scanning
                )
                messages.success(request, f"Ticket purchased successfully for ₹{price:.2f}. Your balance is now ₹{wallet.balance:.2f}.")
                return redirect('ticket_history') 
            else:
                messages.error(request, f"Insufficient funds. Need ₹{price:.2f} but you only have ₹{wallet.balance:.2f}.")
                
        except Exception as e:
            messages.error(request, f"Error processing ticket purchase: {e}")

    return render(request, 'tickets/buy_ticket.html', {'stations': stations, 'wallet': wallet})

@login_required
def ticket_history(request):
    """Displays a list of the passenger's active and used tickets."""
    # Note: We order by the newest ticket first
    tickets = Ticket.objects.filter(passenger=request.user).order_by('-purchase_time')
    return render(request, 'tickets/ticket_history.html', {'tickets': tickets})