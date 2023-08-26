from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import DateTimeField
from django import forms


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')
    username = forms.CharField(max_length=50, label='Имя пользователя')
    password1 = forms.CharField(max_length=50, label='Пароль')
    password2 = forms.CharField(max_length=50, label='Подтверждение пароля')
    date_joined = DateTimeField(auto_now_add=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1',
                  'password2')
