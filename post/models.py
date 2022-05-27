from distutils.command.upload import upload
from django.db import models
from users.models import UserProfile,MyUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Post(models.Model):
    title=models.TextField(_("Title"),max_length=200,blank=True,null=True)
    image=models.ImageField(_("Image"),upload_to='uploads/',blank=True)
    date_created=models.DateTimeField(_("Date Created"),auto_now=True)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    allowed_friends=models.ManyToManyField(MyUser,related_name='blog_post')

    def __str__(self) -> str:
        return '{} posted {} at {}'.format(self.user.email,self.title,self.date_created)