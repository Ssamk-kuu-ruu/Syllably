import re
from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check authenticated users
        if request.user.is_authenticated:
            # Allow them to access the password change pages, static assets, and logout
            allowed_urls = [
                reverse('password_change'),
                reverse('password_change_done'),
                reverse('logout'),
            ]
            
            # If they are trying to go somewhere else, check their password status
            if request.path not in allowed_urls and not request.path.startswith('/static/'):
                # Check if the username matches the password (since we use Birthday numeric strings)
                # Or check if the password is purely an 8-digit numeric birthday string (MMDDYYYY)
                is_numeric_birthday = re.match(r'^\d{8}$', request.user.username) or hasattr(request.user, 'profile') and request.user.profile.needs_password_change
                
                # Alternate highly reliable Django method: 
                # Check if the user's password can be verified using their raw username/birthday format
                if request.user.check_password(request.user.username): 
                    return redirect('password_change')

        response = self.get_response(request)
        return response