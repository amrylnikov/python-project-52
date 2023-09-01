from django.contrib.auth.models import User


class New_Display_User(User):

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
