from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# from task_manager.users.models import New_Display_User


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')
    username = forms.CharField(
        max_length=50,
        label='Имя пользователя',
        help_text='''Обязательное поле. Не более 150 символов. Только буквы,
        цифры и символы @/./+/-/_.'''
    )
    password1 = forms.CharField(
        max_length=50,
        label='Пароль',
        help_text='Ваш пароль должен содержать как минимум 3 символа.'
    )
    password2 = forms.CharField(
        max_length=50,
        label='Подтверждение пароля',
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1',
                  'password2')
