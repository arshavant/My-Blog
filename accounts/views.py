from django.shortcuts import render, redirect
from django.views import View
from .forms import SignupForm, LoginForm
from .models import Account

# Create your views here.


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

            if not Account.objects.filter(email=email).exists() and password == confirm_password:
                new_account = Account(
                    username=username,
                    email=email,
                    password=password,
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

            if user_account.exists() and user_account.filter(password=password).exists():
                request.session['is_logged_in'] = True
                request.session['logged_account_id'] = user_account.filter(pk=user_account.first().pk).first().pk

                return redirect('home')
            elif not user_account.exists():
                return redirect('signup')
            elif not user_account.filter(password=password).exists():
                return redirect('login')

        return render(request, "accounts/login.html", {
            'login_form': login_form,
        })
