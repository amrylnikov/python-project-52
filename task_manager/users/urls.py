from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.show_users, name='users'),
    path('create', views.register_user, name='registration'),
    path('<int:id>/edit/', views.edit_user, name='edit'),
    path('<int:id>/delete/', views.delete_user, name='delete'),
]
