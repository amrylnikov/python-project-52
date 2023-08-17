from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path('', views.StatusShow.as_view(), name='statuses'),
    path('create/', views.StatusCreate.as_view(), name='create_status'),
    path('<int:pk>/edit/', views.StatusEdit.as_view(), name='edit_status'),
    path('<int:pk>/delete/', views.StatusDelete.as_view(), name='delete_status'),
]
