from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Post, Category, Author

class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20, widget=forms.Textarea, label="Текст")
    
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        label="Автор"
    )
    
    categories = forms.ModelMultipleChoiceField(
        # queryset=Category.objects.values_list('name', flat=True),
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Категории"
    )

    class Meta:
        model = Post
        fields = ['author', 'post_type', 'categories', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Текст не должен быть идентичен заголовку."
            )

        return cleaned_data