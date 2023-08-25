from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.UsersShow.as_view(), name='users'),
    path('create/', views.UserRegister.as_view(), name='registration'),
    # path('<int:pk>/edit/', views.UserEdit.as_view(), name='edit'),
    path(r'^(?P<pk>\d+)/edit/$', views.UserEdit.as_view(), name='edit'),
    path('<int:pk>/delete/', views.UserDelete.as_view(), name='delete'),
]
