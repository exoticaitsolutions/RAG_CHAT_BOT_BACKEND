from functools import wraps
from django.shortcuts import redirect

def custom_login_required(view_func):
    print('view_func', view_func)
    """
    Custom login required decorator for MVC-based Django structure.
    Redirects to '/login/' if the user is not authenticated.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        print('custom_login_required',request.user.is_authenticated)
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
        print('redirect_if_authenticated',request.user.is_authenticated)
        if request.user.is_authenticated:
            return redirect('/dashboard/')  # Redirect logged-in users
        return view_func(request, *args, **kwargs)
    return wrapper
