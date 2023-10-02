from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, ("Your account has been created and you're now logged in...")
            )
            return redirect("main_app:index")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        # Assuming you have a login form, replace LoginForm with your actual form
        # Here, LoginForm should include fields for username and password
        form = AuthenticationForm(request, data=request.POST)
        print(f"Form data: {request.POST}")  # Debugging line
        print(f"Form errors: {form.errors}")
        if form.is_valid():
            user = form.get_user()
            print(f"form is valid ran")
            if user:
                login(request, user)
                print(f"Request: {request}   ---   user: {user}")
                messages.success(request, ("You're now logged in."))
                return redirect(
                    "main_app:index"
                )  # Replace 'home' with your desired redirect URL
        else:
            print("form is invalid")
    else:
        # Initialize an instance of your login form
        print(f"Else ran.")
        form = AuthenticationForm(request, data=request.POST)

    return render(request, "users/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, ("You've been logged out."))
    return redirect("main_app:index")
