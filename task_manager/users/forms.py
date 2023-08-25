from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import DateTimeField
from django import forms


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    date_joined = DateTimeField(auto_now_add=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1',
                  'password2')
