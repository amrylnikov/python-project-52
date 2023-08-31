from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from task_manager import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('admin/', admin.site.urls),
]
