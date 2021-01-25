from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'author', 'post']
        labels = {
            "body": "Treść Komentarza",
        }
    def __init__(self, *args, **kwargs):
        super(CommentCreateForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = forms.HiddenInput()
        self.fields['post'].widget = forms.HiddenInput()
