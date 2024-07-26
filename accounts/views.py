import os
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignupForm, LoginForm, UsernameChangeForm, EmailChangeForm, PasswordChangeForm
from .models import Account
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Create your views here.

load_dotenv()
fernet = Fernet(os.getenv('fernet_key').encode())


class SignupView(View):
    def get(self, request):
        signup_form = SignupForm()

        return render(request, "accounts/sign-up.html", {
            'signup_form': signup_form,
        })

    def post(self, request):
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            username = f"{signup_form.cleaned_data['first_name']} {signup_form.cleaned_data['last_name']}"
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            confirm_password = signup_form.cleaned_data['confirm_password']

            encrypted_password = fernet.encrypt(password.encode()).decode('utf-8')

            if not Account.objects.filter(email=email).exists() and password == confirm_password:
                new_account = Account(
                    username=username,
                    email=email,
                    password=encrypted_password,
                )
                new_account.save()

                request.session['is_logged_in'] = True
                request.session['logged_account_id'] = new_account.pk

                return redirect('home')
            elif Account.objects.filter(email=email).exists():
                return redirect('login')

        return render(request, "accounts/sign-up.html", {
            'signup_form': signup_form,
        })


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()

        return render(request, "accounts/login.html", {
            'login_form': login_form,
        })

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            user_account = Account.objects.filter(email=email)
            user_password = user_account.get().password

            decrypted_password = fernet.decrypt(user_password.encode()).decode('utf-8')

            if user_account.exists() and password == decrypted_password:
                request.session['is_logged_in'] = True
                request.session['logged_account_id'] = user_account.filter(pk=user_account.first().pk).first().pk

                return redirect('home')
            elif not user_account.exists():
                return redirect('signup')

        return render(request, "accounts/login.html", {
            'login_form': login_form,
        })


class UserProfileView(View):
    def get(self, request):
        user_account_id = request.session.get('logged_account_id')
        user_account = Account.objects.filter(pk=user_account_id).first()

        return render(request, "accounts/profile.html", {
            'account': user_account,
        })

    def post(self, request):
        request.session['is_logged_in'] = False

        return redirect('home')


class UsernameChangeView(View):
    def get(self, request):
        username_change_form = UsernameChangeForm()

        return render(request, "accounts/change-username.html", {
            'username_change_form': username_change_form,
        })

    def post(self, request):
        user_account_id = request.session.get('logged_account_id')

        user_account = Account.objects.filter(pk=user_account_id).first()
        username_change_form = UsernameChangeForm(request.POST)

        if username_change_form.is_valid():
            username = username_change_form.cleaned_data['username']

            user_account.username = username
            user_account.save()

            return redirect('home')

        return render(request, "accounts/change-username.html", {
            'username_change_form': username_change_form,
        })


class EmailChangeView(View):
    def get(self, request):
        email_change_form = EmailChangeForm()

        return render(request, "accounts/change-email.html", {
            'email_change_form': email_change_form,
        })

    def post(self, request):
        email_change_form = EmailChangeForm(request.POST)

        user_account_id = request.session.get('logged_account_id')
        user_account = Account.objects.filter(pk=user_account_id).first()

        if email_change_form.is_valid():
            email = email_change_form.cleaned_data['email']

            user_account.email = email
            user_account.save()

            return redirect('home')

        return render(request, "accounts/change-email.html", {
            'email_change_form': email_change_form,
        })


class PasswordChangeView(View):
    def get(self, request):
        password_change_form = PasswordChangeForm()

        return render(request, "accounts/change-password.html", {
            'password_change_form': password_change_form,
        })

    def post(self, request):
        password_change_form = PasswordChangeForm(request.POST)

        account_account_id = request.session.get('logged_account_id')
        user_account = Account.objects.filter(pk=account_account_id).first()
        current_encrypted_password = user_account.password.encode()
        current_decrypted_password = fernet.decrypt(current_encrypted_password).decode('utf-8')

        if password_change_form.is_valid():
            old_password = password_change_form.cleaned_data['old_password']
            new_password = password_change_form.cleaned_data['new_password']
            new_password_confirm = password_change_form.cleaned_data['new_password_confirm']

            if old_password == current_decrypted_password and new_password == new_password_confirm:
                new_encrypted_password = fernet.encrypt(new_password.encode()).decode('utf-8')

                user_account.password = new_encrypted_password
                user_account.save()

                return redirect('home')

            return render(request, 'accounts/change-password.html', {
                'password_change_form': password_change_form,
            })
