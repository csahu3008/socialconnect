
from .models import MyUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,ReadOnlyPasswordHashField
from django import forms
class  MyUserForm(forms.ModelForm):
    class Meta:
        model=MyUser
        fields=('mobile','email','name',)
    mobile=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'class':'form-control'}))
    name=forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'id':'password1','class':'form-control'}))
    password1=forms.CharField(max_length=30,help_text=_('Please Enter the same password as before'), widget=forms.PasswordInput(attrs={'class':'form-control','id':'password1'}))
    def clean_password1(self):
        cd=self.cleaned_data
        password=cd['password']
        password1=cd['password1']
        if password != password1:
            raise ValidationError(_('Password do not match'))
    def save(self,commit=True):
        user=super().save(commit=False)
        print('came inside0')
        user.set_password(self.cleaned_data.get('password'))       
        if commit:
            print('hello')
            user.save()
        return user

class MyUserChangeForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields =('name','email','password','user_permissions') 
    password=ReadOnlyPasswordHashField()
    def clean_password(self):
        return self.initial['password']

class loginform(forms.Form):
    mobile=forms.CharField(max_length=40,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(max_length=40,required=False,widget=forms.EmailInput(attrs={'class':'form-control'}))
    password=forms.CharField(max_length=40,widget=forms.PasswordInput(attrs={'class':'form-control'}))