from django import forms
from django.contrib.auth.models import User
from .models import Comment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment content cannot be empty.")
        return content