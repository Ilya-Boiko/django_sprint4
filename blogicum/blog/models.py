from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text='Снимите галочку, '
                                       'чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True  # Указываем, что это абстрактная модель


class Post(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок',
                             help_text='Введите заголовок публикации.')
    text = models.TextField(verbose_name='Текст',
                            help_text='Введите текст публикации.')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='Если установить дату и время '
                                    'в будущем — можно делать '
                                    'отложенные публикации.')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория'
    )
    image = models.ImageField(upload_to='post_images/',
                              blank=True, null=True,
                              verbose_name='Изображение')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Category(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок',
                             help_text='Введите заголовок категории.')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                            'разрешены символы латиницы, '
                            'цифры, дефис и подчёркивание.')
    description = models.TextField(verbose_name='Описание',
                                   help_text='Введите описание категории.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(max_length=256, verbose_name='Название места',
                            help_text='Введите название места.')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время добавления')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Публикация')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']  # Сортировка по времени создания

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post.title}'
