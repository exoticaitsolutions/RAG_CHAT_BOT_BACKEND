from functools import wraps
from django.shortcuts import redirect

def custom_login_required(view_func):
    """
    Custom login required decorator for MVC-based Django structure.
    Redirects to '/login/' if the user is not authenticated.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')  # Redirect unauthorized users
        return view_func(request, *args, **kwargs)
    return wrapper



def redirect_if_authenticated(view_func):
    """
    Redirects logged-in users away from login/register pages.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/dashboard/')  # Redirect logged-in users
        return view_func(request, *args, **kwargs)
    return wrapper
