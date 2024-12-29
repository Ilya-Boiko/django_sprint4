from django.urls import path
from . import views  # Импортируем views из текущего приложения

app_name = 'pages'

urlpatterns = [
    path('about/', views.about, name='about'),  # Страница "О нас"
    path('rules/', views.rules, name='rules'),  # Страница "Правила"
]
