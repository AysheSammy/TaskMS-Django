from django.urls import path
from .views import ToDoList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage, ToDoListDelete, ToDoListUpdate, ToDoListCreate, ToDoListdetail
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    
    path('', ToDoList.as_view(), name='tasks'),
    path('task-list/<int:pk>/', ToDoListdetail.as_view(), name='task-list'),
    path('task-list-update/<int:pk>/', ToDoListUpdate.as_view(), name='task-list-update'),
    path('task-list-create/', ToDoListCreate.as_view(), name='task-list-create'),
    path('task-list-delete/<int:pk>/', ToDoListDelete.as_view(), name='task-list-delete'),

    path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('task-list/<int:task_list_id>/create', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
]
