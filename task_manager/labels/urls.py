from django.urls import path

from task_manager.labels import views

urlpatterns = [
    path('', views.LabelShow.as_view(), name='labels'),
    path('create/', views.LabelCreate.as_view(), name='create_label'),
    path('<int:pk>/update/', views.LabelEdit.as_view(), name='edit_label'),
    path('<int:pk>/delete/',
         views.LabelDelete.as_view(),
         name='delete_label'),
]
