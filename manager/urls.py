from django.urls import path

from .views import TaskCreateView, TaskView, SingleTaskView, delete_task, ApiDocView

app_name = 'manager'
urlpatterns = [
    path('', TaskView.as_view(), name='tasks'),
    path('task/<int:pk>/', SingleTaskView.as_view(), name='task'),
    path('task/add/', TaskCreateView.as_view(), name='add-task'),
    path('delete-task/<int:task_id>/', delete_task, name='delete-task'),
    path('api-documentation/', ApiDocView.as_view(), name='api-doc')
]
