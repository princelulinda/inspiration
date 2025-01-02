from django.contrib import admin
from .models import Article, Category, Tag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'tags')
    search_fields = ('title', 'content')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
