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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Включаем маршруты приложения blog
    # Включаем маршруты приложения pages
    path('pages/', include('pages.urls')),
    # Подключаем маршруты для аутентификации
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/registration/', views.registration, name='registration'),  # Страница регистрации
    path('profile/<str:username>/', views.profile, name='profile'),  # Страница профиля пользователя
]
