from .models import MyUser,UserProfile
from .forms import MyUserChangeForm,MyUserForm
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CustomAdmin(UserAdmin):
    add_form=MyUserForm
    list_display=['mobile','email','name']
    form=MyUserChangeForm
    ordering=('mobile','name','email')
    add_fieldsets=((None,{'classes':('wide',),'fields':('name','mobile','email','password','password1','is_superuser','is_active','is_staff')}),)
    fieldsets=((None,{'fields':('mobile','email','password')}),('Designation',{'fields':('is_superuser','is_staff')}),('User Permissions',{'fields':('user_permissions',)}),)
    # fieldsets=(
    #     (None,{'fields':('email','password','mobile')}),('Designation',{'fields':('is_active','is_superuser','is_staff')}),('User Permissions',{'fields':('user_permissions',)})
    # )
    search_fields=('mobile',)
admin.site.register(MyUser,CustomAdmin)
admin.site.register(UserProfile)

# admin.site.index_title='Menu'
# admin.site.site_url='myadmin'
# admin.site.site_title='News and Weather'
# admin.site.site_index='my site'
# admin.site.site_header='News @ waether'