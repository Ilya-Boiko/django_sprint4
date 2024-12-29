from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from datetime import datetime
from django.http import Http404


def index(request):
    # Получаем пять последних опубликованных постов,
    # которые соответствуют условиям
    posts = Post.objects.filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]  # Сортируем по дате и берем последние 5
    context = {
        'post_list': posts
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, pub_date__lte=datetime.now(),
                             is_published=True)
    # Проверяем, что категория также опубликована
    if not post.category.is_published:
        raise Http404("Категория не найдена.")

    context = {
        'post': post
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    # Получаем опубликованные посты, относящиеся к данной категории
    category_posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=datetime.now()
    )
    context = {
        'category': category,
        'post_list': category_posts
    }
    return render(request, 'blog/category.html', context)
