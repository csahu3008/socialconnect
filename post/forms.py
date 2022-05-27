from email.mime import image
from django import forms
from django.db import models
from .models import Post
from users.models import MyUser,UserProfile
from django.utils.translation import gettext_lazy as _

class CreatePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['title', 'image']  
    title=forms.CharField(max_length=400,widget=forms.TextInput(attrs={'class':'f'}))