from django.shortcuts import render
from django.template import context
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email
from django.contrib import messages

User = get_user_model()

from .forms import UserCreateForm, AccountPasswordChangeForm, LoginForm, UserUpdateForm


def register_user(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data["email"]
            user_username = form.cleaned_data["username"]
            user_password = form.cleaned_data["password1"]

            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )

            user.is_active = False
            send_email(user)

            return redirect(reverse("account:email-verification"))
    else:
        form = UserCreateForm()
    return render(request, "account/register.html", {"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("shop:products"))
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                return redirect(reverse("account:dashboard"))
            else:
                messages.info(request, "Invalid username or password")
                return redirect("account:login")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect(reverse("shop:products"))


@login_required
def dashboard_user(request):
    return render(request, "account/dashboard.html")


@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("account:dashboard"))
    else:
        form = UserUpdateForm(instance=request.user)

    context = {"form": form}
    return render(request, "account/profile-management.html", context=context)


@login_required
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        user.delete()
        return redirect(reverse("shop:products"))
    return render(request, "account/account-delete.html")


@login_required
def password_change(request):
    if request.method == "POST":
        form = AccountPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "You successfully change passwrod!")
            return redirect('shop:products')
        else:
            messages.error(request, "Invalid input!")
    else:
        form = AccountPasswordChangeForm(user=request.user)

    context = {"form": form}

    return render(request, "account/change-password.html", context=context)
