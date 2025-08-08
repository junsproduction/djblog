from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('users/', views.user_list, name='users'),
    path('posts/', views.post_management, name='posts'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('posts/<int:post_id>/moderate/', views.moderate_post, name='moderate_post'),
]