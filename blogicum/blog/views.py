from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from datetime import datetime
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone


def index(request):
    # Получаем все опубликованные категории
    published_categories = Category.objects.filter(is_published=True)
    # Получаем все опубликованные посты категории
    posts = Post.objects.filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__in=published_categories
    ).order_by('-pub_date')

    paginator = Paginator(posts, 10)  # 10 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    # Проверяем, что пост опубликован или автор является текущим пользователем
    if not post.is_published and post.author != request.user:
        raise Http404("Пост не найден.")

    # Проверяем, что дата публикации поста меньше или равна текущей дате
    if post.pub_date > timezone.now() and post.author != request.user:
        raise Http404("Пост не найден.")

    # Если пост не опубликован, но автор - текущий пользователь,
    # показываем пост
    if not post.is_published and post.author == request.user:
        comments = post.comments.all()  # Получаем все комментарии к посту
        form = CommentForm()  # Создаем экземпляр формы комментария

        context = {
            'post': post,
            'comments': comments,
            'form': form,  # Передаем форму в контекст
        }
        return render(request, 'blog/detail.html', context)

    comments = post.comments.all()  # Получаем все комментарии к посту
    form = CommentForm()  # Создаем экземпляр формы комментария

    context = {
        'post': post,
        'comments': comments,
        'form': form,  # Передаем форму в контекст
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)
    # Получаем опубликованные посты, относящиеся к данной категории
    category_posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=datetime.now()
    ).order_by('-pub_date')  # Добавлено сортировка по дате публикации
    paginator = Paginator(category_posts, 10)  # 10 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj  # Изменено с 'post_list' на 'page_obj'
    }
    return render(request, 'blog/category.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Перенаправление на страницу входа после успешной регистрации
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html',
                  {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    # Получаем все публикации автора, включая удаленные
    posts = Post.objects.filter(author=user).order_by(
        '-pub_date')  # Отображаем все публикации
    paginator = Paginator(posts, 10)  # 10 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user': user,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Обработка файлов
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Установите автора
            post.save()
            # Перенаправление на страницу профиля
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Проверяем, что текущий пользователь является автором поста
    if post.author != request.user:
        # Перенаправление на страницу просмотра поста
        return redirect('post_detail', id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES,
                        instance=post)  # Обработка файлов
        if form.is_valid():
            form.save()
            # Перенаправление на страницу отредактированной публикации
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)

    # Используем тот же шаблон, что и для создания поста
    return render(request, 'blog/create.html', {'form': form})


def post_list(request):
    posts = Post.objects.all().order_by('-pub_date')  # Получаем все посты
    paginator = Paginator(posts, 10)  # 10 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Используем create.html
    return render(request, 'blog/create.html',
                  {'form': None, 'posts': page_obj})


@login_required
def edit_profile(request, username):
    # Получаем пользователя по имени
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        # Обновляем поля пользователя
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')  # Добавлено поле email

        # Сохраняем изменения в базе данных
        user.save()
        # Перенаправление на страницу профиля
        return redirect('blog:profile', username=user.username)

    context = {
        'form': {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,  # Добавлено поле email
        }
    }
    return render(request, 'registration/edit_profile.html', context)


@login_required
def main_page(request):
    posts = Post.objects.filter(is_published=True).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/main_page.html', {'page_obj': page_obj})


@login_required
def profile_page(request):
    posts = Post.objects.filter(author=request.user).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/profile_page.html', {'page_obj': page_obj})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Проверяем, что текущий пользователь является автором поста
    if post.author == request.user:
        post.delete()  # Удаляем пост
        return redirect('blog:index')  # Перенаправление на главную страницу
    else:
        # Перенаправление на страницу просмотра поста
        return redirect('post_detail', id=post.id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/detail.html', {'form': form, 'post': post})


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment.html',
                  {'form': form, 'comment': comment})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author == request.user:
        comment.delete()
        return redirect('blog:post_detail', id=post_id)
    else:
        return redirect('blog:post_detail', id=post_id)


def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Перенаправление на страницу профиля с именем пользователя
            return redirect('blog:profile', username=user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
