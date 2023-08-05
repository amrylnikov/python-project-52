from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.index),
    path('login_user', views.login, name='login'),
]
