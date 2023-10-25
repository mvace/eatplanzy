from .forms import (
    CustomUserCreationForm,
    UserProfileForm,
    UpdateUserForm,
    CustomAuthenticationForm,
    MessageForm,
)
from .models import UserProfile
from recipe.models import Recipe
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Conversation, Message
from django.db.models import Q


# Create your views here.


@login_required
def conversation(request, pk):
    sender = User.objects.get(id=request.user.id)
    receiver = User.objects.get(id=pk)

    conversation = (
        Conversation.objects.filter(participants=sender)
        .filter(participants=receiver)
        .first()
    )

    form = MessageForm()
    if pk == request.user.id:
        messages.error(request, "You cannot message yourself.")
        return redirect(request.META.get("HTTP_REFERER"))

    if conversation is not None:
        communication = Message.objects.filter(conversation=conversation)
        if request.method == "POST":
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.conversation = conversation
                message.sender = sender
                message.receiver = receiver
                message.save()
                form = MessageForm()
            else:
                form = MessageForm()

    else:
        new_conversation = Conversation.objects.create()
        new_conversation.participants.add(sender, receiver)

        communication = []  # Initialize an empty list for communication
        form = MessageForm()

    context = {
        "conversation": conversation,
        "communication": communication,
        "form": form,
    }

    return render(request, "users/conversation.html", context)


def profile_view(request, pk):
    profile = UserProfile.objects.get(user_id=pk)
    profile_recipes = Recipe.objects.filter(chef_id=pk)
    return render(
        request,
        "users/profile.html",
        {"profile": profile, "profile_recipes": profile_recipes},
    )


@login_required
def update_profile(request):
    current_user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user_id=request.user.userprofile.user_id)
    profile_form = UserProfileForm(
        request.POST or None, request.FILES or None, instance=user_profile
    )
    user_form = UpdateUserForm(
        request.POST or None, request.FILES or None, instance=current_user
    )

    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ("Your Profile Has Been Updated."))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "There was an error in the form submission.")

    else:
        profile_form = UserProfileForm(instance=user_profile)

    return render(
        request,
        "users/update_profile.html",
        {"profile_form": profile_form, "user_form": user_form},
    )


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
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, ("You're now logged in."))
                return redirect("main_app:index")

    else:
        form = CustomAuthenticationForm(request)

    return render(request, "users/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, ("You've been logged out."))
    return redirect("main_app:index")
