from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path('', views.TaskShow.as_view(), name='tasks'),
    path('create/', views.TaskCreate.as_view(), name='create_task'),
    path('<int:pk>/update/', views.TaskEdit.as_view(), name='edit_task'),
    path(
        '<int:pk>/delete/', views.TaskDelete.as_view(), name='delete_task'
    ),
    path('<int:pk>/', views.TaskGetInfo.as_view(), name='get_task'),
]
