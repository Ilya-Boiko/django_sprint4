"""blogicum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# Импортируем include для включения маршрутов приложений
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Импортируем представления для аутентификации
from blog import views  # Импортируем views из приложения blog
from django.conf.urls import handler404, handler403, handler500
from pages.views import custom_403_view, custom_404_view, custom_500_view
from django.conf import settings
from django.conf.urls.static import static

# Убедитесь, что обработчики ошибок определены
handler404 = 'pages.views.custom_404_view'
handler403 = 'pages.views.custom_403_view'
handler500 = 'pages.views.custom_500_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Включаем маршруты приложения blog
    # Включаем маршруты приложения pages
    path('pages/', include('pages.urls')),
    # Подключаем маршруты для аутентификации
    path('auth/', include('django.contrib.auth.urls')),  # Измените на 'auth/'
    path('auth/registration/', views.registration, name='registration'),  # Измените на 'auth/registration/'
    path('profile/<str:username>/', views.profile, name='profile'),  # Страница профиля пользователя
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),  # Добавьте этот маршрут
    path('posts/create/', views.create_post, name='create_post'),  # Добавлено для создания поста
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),  # Добавлено для редактирования поста
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
