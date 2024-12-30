from django.urls import path, include  # Импортируем include
from . import views  # Импортируем views из текущего приложения

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('posts/<int:id>/', views.post_detail,
         name='post_detail'),  # Детали поста
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),  # Посты по категории
    path('posts/create/', views.create_post,
         name='create_post'),  # Страница создания поста
    path('posts/<int:post_id>/edit/', views.edit_post,
         name='edit_post'),  # Страница редактирования поста
    path('posts/<int:post_id>/delete/', views.delete_post,
         name='delete_post'),  # Страница удаления поста
    path('profile/<str:username>/', views.profile,
         name='profile'),  # Страница профиля пользователя
    path('auth/registration/', views.registration,
         name='registration'),  # Страница регистрации
    path('profile/<str:username>/edit/', views.edit_profile,
         name='edit_profile'),  # Добавьте этот маршрут
    # Подключаем стандартные пути аутентификации
    path('auth/', include('django.contrib.auth.urls')),
    path('posts/<int:post_id>/comment/', views.add_comment,
         name='add_comment'),  # Добавление комментария
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),  # Удаление комментария
]
