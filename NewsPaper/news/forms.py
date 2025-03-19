from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from pytz import common_timezones
from .resources import POSITIONS
from .models import Post, Category, Author

class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20, widget=forms.Textarea, label=_("Text"))
    
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        label=_("Author")
    )
    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=_("Categories")
    )

    post_type = forms.ChoiceField( 
        choices=POSITIONS,
        label=_("Type")
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
                _("The text should not be identical to the title.")
            )

        return cleaned_data

class TimezoneForm(forms.Form):
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in common_timezones], label=_("Select Timezone"))