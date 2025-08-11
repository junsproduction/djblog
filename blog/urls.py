from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category_posts, name='category-posts'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post-edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('post/new/', views.post_new, name='post-new'),
    path('my-posts/', views.my_posts, name='my-posts'),
]
