from  django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from .models import Post
from django import forms
from django.contrib.auth.models import User

class PostFilter(FilterSet):
    author = ModelMultipleChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        label='Author',
        widget=forms.CheckboxSelectMultiple,
    )
    created_at =DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }
