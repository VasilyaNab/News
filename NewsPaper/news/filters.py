from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, CharFilter
from .models import Post
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _ 

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label=_('Enter the title'),
    )
    author = ModelMultipleChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        label=_('Author'),
        widget=forms.CheckboxSelectMultiple,
    )
    created_at = DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label=_('Publication date'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Post
        fields = []