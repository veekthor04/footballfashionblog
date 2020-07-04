from django import forms
from .models import Category

class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!",
            'style': 'height: 8em;'
        })
    )

class TagForm(forms.Form):
    tag = forms.ModelMultipleChoiceField( widget = forms.CheckboxSelectMultiple(attrs={'id': 'tag'}), required=False, queryset = Category.objects.all())
