from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.utils import timezone 

# We need these from other apps:
from metroline.models import Station
from tickets.models import Ticket

# Custom decorator to check if the user belongs to the 'Scanners' group
def is_scanner(user):
    return user.groups.filter(name='Scanners').exists()

@login_required
@user_passes_test(is_scanner, login_url='/login/') # Only scanners can access this view
def scanner_interface(request):
    """Main interface for scanners to input ticket IDs."""
    return render(request, 'scanner/scanner_interface.html', {})

@login_required
@user_passes_test(is_scanner, login_url='/login/')
@transaction.atomic
def scan_ticket(request):
    """Handles the logic for scanning a ticket for entry or exit."""
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id', '').strip()
        
        try:
            # We look up the ticket by the ID provided by the scanner
            ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
            
            # 1. Entry Scan (Active -> In Use)
            if ticket.status == 'Active' and not ticket.entry_scan_time:
                ticket.status = 'In Use'
                ticket.entry_scan_time = timezone.now()
                ticket.save()
                messages.success(request, f"Entry Granted for Ticket {ticket_id}. Status: In Use.")

            # 2. Exit Scan (In Use -> Used)
            elif ticket.status == 'In Use' and ticket.entry_scan_time and not ticket.exit_scan_time:
                ticket.status = 'Used'
                ticket.exit_scan_time = timezone.now()
                ticket.save()
                messages.success(request, f"Exit Recorded for Ticket {ticket_id}. Status: Used.")

            # 3. Handle Invalid States
            elif ticket.status == 'Used':
                messages.error(request, f"Ticket {ticket_id} is already Used.")
            elif ticket.status == 'Expired':
                messages.error(request, f"Ticket {ticket_id} is Expired.")
            else:
                messages.error(request, f"Invalid ticket state for scanning.")
        
        except Ticket.DoesNotExist:
            messages.error(request, f"Error: Ticket ID {ticket_id} not found.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    return redirect('scanner_interface') # Redirect back to the scanner interface

@login_required
@user_passes_test(is_scanner, login_url='/login/')
def offline_purchase(request):
    """Allows scanner to create a new ticket that is immediately marked as Used."""
    stations = Station.objects.all().order_by('name')

    if request.method == 'POST':
        start_station_id = request.POST.get('start_station')
        end_station_id = request.POST.get('end_station')
        
        if not start_station_id or not end_station_id:
            messages.error(request, "Please select both a start and end station.")
            return redirect('offline_purchase')
            
        try:
            start_station = get_object_or_404(Station, id=start_station_id)
            end_station = get_object_or_404(Station, id=end_station_id)
            
            # Create the ticket. Since this is offline/cash, we mark it USED immediately.
            Ticket.objects.create(
                passenger=request.user, # Assigns to the scanner user for tracking
                start_station=start_station,
                end_station=end_station,
                price=5.00, # Simple flat rate for cash purchase
                status='Used' 
            )
            messages.success(request, "Offline Ticket created and marked as USED immediately.")
            return redirect('offline_purchase')
            
        except Exception as e:
            messages.error(request, f"Error creating ticket: {e}")

    return render(request, 'scanner/offline_purchase.html', {'stations': stations})