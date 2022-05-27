from django.db import models
from django.utils.translation import gettext_lazy as _

# from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
 
class CustomManager(BaseUserManager):
    def create_user(self,mobile,email,name,password='None',**kwargs):
        if not mobile:
            raise ValueError(" Mobile Number is essiential for registration")
        email=self.normalize_email(email)
        user=self.model(mobile=mobile,email=email,name=name,**kwargs)
        user.set_password(password)
        user.save()    
        return user
        
    def create_superuser(self,mobile,email,name,password,**kwargs):
        kwargs.setdefault('is_superuser',True)
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_active',True)
        if kwargs.get('is_superuser') is not True:
            raise ValueError("user Must be Superuser")
        if kwargs.get('is_staff') is not True:
            raise ValueError("user must be staff")
        if kwargs.get('is_active') is not True:
            raise ValueError("User must be active")
        self.create_user(mobile,email,name,password,**kwargs)    

class MyUser(AbstractUser):
    mobile=models.CharField(_('Mobile Number'),max_length=10,unique=True)
    email=models.EmailField(_('Email'),max_length=20)
    name=models.CharField(_('Name'),max_length=30)
    username=None
    EMAIL_FIELD='email'
    USERNAME_FIELD='mobile'
    REQUIRED_FIELDS=['email','name']
    def __str__(self):
        return '{} is registered with {}'.format(self.name,self.mobile)
    class Meta:
        verbose_name_plural='MyUsers'
    objects=CustomManager()



class UserProfile(models.Model):
    bio=models.TextField(_("Bio"),max_length=200,blank=True,null=True)
    user=models.OneToOneField(MyUser,on_delete=models.CASCADE)
    friends=models.ManyToManyField(MyUser,related_name='profile')

    def __str__(self) -> str:
        return '{} has {} friends '.format(self.user.email,self.friends.all().count())

@receiver(post_save, sender=MyUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save() 