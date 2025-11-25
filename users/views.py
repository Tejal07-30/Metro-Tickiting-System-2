from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# The main dashboard/home page. Only accessible if user is logged in.
@login_required
def home(request):
    # This renders the home template, which checks the user's groups to show specific links.
    return render(request, 'users/home.html', {})
