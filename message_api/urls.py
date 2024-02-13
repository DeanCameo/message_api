from django.urls import path
from .views import write_message, get_all_messages, get_unread_messages, read_message, delete_message, register_user, login

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login, name='login_user'),
    path('write_message/', write_message, name='write_message'),
    path('get_all/<str:user>/', get_all_messages, name='get_all_messages'),
    path('get_unread/<str:user>/', get_unread_messages, name='get_unread_messages'),
    path('read/<int:pk>/', read_message, name='read_message'),
    path('delete/<int:pk>/', delete_message, name='delete_message'),
]
