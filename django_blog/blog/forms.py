from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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

class UserRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=True, label='Name')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('name', 'email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Store the entered name and email on the user object
        user.first_name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Comma-separated tags")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'image']
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