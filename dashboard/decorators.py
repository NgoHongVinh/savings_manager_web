from django.shortcuts import redirect

def customer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if not hasattr(request.user, "customer"):
            return redirect("admin")

        return view_func(request, *args, **kwargs)

    return wrapper

def employee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if not hasattr(request.user, "employee"):
            return redirect("profile")

        return view_func(request, *args, **kwargs)

    return wrapper