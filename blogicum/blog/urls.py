from django.urls import path
from . import views  # Импортируем views из текущего приложения

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('posts/<int:id>/', views.post_detail,
         name='post_detail'),  # Детали поста
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),  # Посты по категории
]
