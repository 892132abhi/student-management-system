from django.shortcuts import redirect
from functools import wraps

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role.lower() != 'student':
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return wrapper