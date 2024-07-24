from django import forms


class SignupForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', max_length=100)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=100)
