from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.ShowUsers.as_view(), name='users'),
    path('create', views.RegisterUser.as_view(), name='registration'),
    path('<int:id>/edit/', views.EditUser.as_view(), name='edit'),
    path('<int:id>/delete/', views.DeleteUser.as_view(), name='delete'),
]
