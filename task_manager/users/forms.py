from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

from task_manager.users.models import User


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1',
                  'password2')
