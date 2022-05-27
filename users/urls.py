from django.urls import path
from .views import signup,Login,SeeUsers,AddUserAsFriend,ShowUserProfile
urlpatterns = [
    path('signup/',signup,name='signup'),
    path('login/',Login,name='login'),
    path('view_users/',SeeUsers.as_view(),name='see_users'),
    path('add_user/',AddUserAsFriend.as_view(),name='add_friend'),
    path('profile/<int:pk>/',ShowUserProfile.as_view(),name='profile'),

]
