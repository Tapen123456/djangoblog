from django.urls import path
from . import views
from .views import (
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    RegisterView,
    MyPostsView,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('my-posts/', MyPostsView.as_view(), name='my_posts'),
    path('register/', RegisterView.as_view(), name='register'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]