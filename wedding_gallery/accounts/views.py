from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import GuestUser
from .forms import GuestLoginForm

def guest_login(request):
    # Allow multiple logins/registrations as per user request
    # if request.session.get('guest_id'):
    #    return redirect('gallery:home')

    if request.method == "POST":
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Always create a new guest user to log the entry
            guest = GuestUser.objects.create(
                email=email,
                username=email.split('@')[0],
                cookies_accepted=True
            )
            # Set session
            request.session['guest_id'] = guest.id
            request.session.set_expiry(60*60*24*30) # 30 days
            return redirect('gallery:home')
    else:
        form = GuestLoginForm()

    return render(request, 'accounts/guest_login.html', {'form': form})

def photographer_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('uploads:dashboard')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('uploads:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/photographer_login.html', {'form': form})

def photographer_logout(request):
    logout(request)
    return redirect('landing_page')
