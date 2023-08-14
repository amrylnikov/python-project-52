from django.contrib import admin
from django.urls import path, include

from task_manager import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('', include('django.contrib.auth.urls')),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('users/', include('task_manager.users.urls')),
    path('admin/', admin.site.urls),
]
