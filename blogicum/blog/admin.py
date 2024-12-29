from django.contrib import admin
from .models import Post, Category, Location

admin.site.empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Регистрируем модели с настройками админки:
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
