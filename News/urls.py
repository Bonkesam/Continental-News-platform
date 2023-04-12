from django.urls import path
from . import views

urlpatterns = [
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('', views.home, name='home'),
    path('search/', views.search_articles, name='search_articles'),
    path('articles/create/', views.create_article, name='create_article'),
]
