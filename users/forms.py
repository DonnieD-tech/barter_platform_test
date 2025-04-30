from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Пароли не совпадают.")

        # Проверка на существование пользователя с таким же именем или email
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError("Пользователь с таким email уже существует.")

        return cleaned_data