# f:\PyCharm\django\my_project\myapp\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('create/', views.create_article, name='create_article'),
    path('<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/like/', views.like_article, name='like_article'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]