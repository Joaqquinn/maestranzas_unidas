from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  # o la URL que uses

            user_profile = getattr(request.user, 'profile', None)

            if user_profile and user_profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            return redirect('sin_permiso')  # crea esta vista/template para mostrar mensaje de error
        return wrapper
    return decorator
