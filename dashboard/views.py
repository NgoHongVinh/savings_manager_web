from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import EmailChangeForm
from django.contrib import messages

from .utils import read_session_errors


@login_required
def profile(request):
    if request.method == "POST":
        if request.POST.get("form_type") == "password":
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                messages.success(request, "Password updated successfully.")
                update_session_auth_hash(request, user)
            else:
                request.session["password_errors"] = password_form.errors

        elif request.POST.get("form_type") == "email":
            email_form = EmailChangeForm(request.POST, user=request.user)

            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successfully.")
            else:
                request.session["email_errors"] = email_form.errors

        return redirect("profile")

    else:
        password_form = PasswordChangeForm(request.user)
        email_form = EmailChangeForm(user=request.user)

        read_session_errors(password_form, request.session, "password_errors")
        read_session_errors(email_form, request.session, "email_errors")

    return render(request, "account/profile.html", {
        "password_form": password_form,
        "email_form": email_form,
    })