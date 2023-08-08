from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.show_users, name='users'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('create', views.register_user, name='registration'),
]
