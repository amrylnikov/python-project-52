from django.contrib.auth.models import User


class Correctly_Displayed_User(User):

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
