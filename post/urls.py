from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import AddPost,HomePage,ShowOtherPosts

urlpatterns = [
    path('add/', AddPost,name='add_post'),
    path('feed/', ShowOtherPosts.as_view(),name='feed'),
    
] 