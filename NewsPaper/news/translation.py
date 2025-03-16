from modeltranslation.translator import translator, TranslationOptions
from .models import Author, Category, Post

class AuthorTranslationOptions(TranslationOptions):
    fields = ('user', 'rating')

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text')

translator.register(Author, AuthorTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Post, PostTranslationOptions)