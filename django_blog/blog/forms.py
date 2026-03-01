from django import forms
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from .models import Comment, Post, Tag


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


class PostForm(forms.ModelForm):
    # Comma-separated tags input, e.g. "health, stress, sleep"
    tags = forms.CharField(required=False, help_text="Comma-separated tags")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            current_tags = self.instance.tags.all()
            self.fields['tags'].initial = ', '.join(tag.name for tag in current_tags)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]

        tag_objects = []
        for name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name=name)
            tag_objects.append(tag_obj)

        if commit:
            instance.tags.set(tag_objects)

        return instance