from django import forms
from .models import Post  # Импортируйте модель Post
from django.contrib.auth.models import User
from .models import Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'pub_date', 'category',
                  'location']  # Убедитесь, что 'image' включено
        widgets = {
            # Удобный виджет для выбора даты и времени
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email']  # Добавлено поле email


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
