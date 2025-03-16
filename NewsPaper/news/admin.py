from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment
from modeltranslation.admin import TranslationAdmin

class PostAdmin(TranslationAdmin):
    list_display = ('title', 'author', 'created_at', 'rating')
    list_filter = ('created_at', 'categories', 'author')
    search_fields = ('title', 'text')
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class AuthorAdmin(TranslationAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user__username',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)