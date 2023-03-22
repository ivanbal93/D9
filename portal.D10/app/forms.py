from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class NewPostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = [
            'post_header',
            'post_text',
            'post_type',
            'author',
            'category'
        ]
    
    def clean(self) -> dict[str, any]:
        cleaned_data = super().clean()

        post_header = cleaned_data.get('post_header')
        if len(post_header) == 0:
            raise ValidationError({"News title can't be empty!"})
        elif post_header is not None and len(post_header) > 64:
            raise ValidationError({"Maximal length of title is 64 symbols!"})
        
        post_text = cleaned_data.get('post_text')
        if len(post_header) == 0:
            raise ValidationError({"Text can't be empty!"})
        
        return cleaned_data