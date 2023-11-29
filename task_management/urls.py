from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from .views import TaskList, TaskDetail, UserListView, UserDetail, UserCreateView

urlpatterns = [
    # path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/tasks/', TaskList.as_view(), name='task-list'),
    path('api/tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/create/', UserCreateView.as_view(), name='user-create'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
