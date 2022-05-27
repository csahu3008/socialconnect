from django.views.generic import CreateView
from django.shortcuts import render,redirect,HttpResponse,reverse,get_object_or_404
from .models import Post
from users.models import MyUser,UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from .forms import CreatePostForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import Settings, settings
from django.urls import reverse_lazy
from django.http import JsonResponse

class HomePage(TemplateView):
    template_name='home.html'


class ShowOtherPosts(LoginRequiredMixin,ListView):
    template_name='OtherPosts.html'
    model=Post
    login_url=reverse_lazy(settings.LOGIN_URL)
    context_object_name='posts'
    def get_queryset(self):
        qs=super().get_queryset().all().filter(allowed_friends=self.request.user).order_by('-date_created')
        return qs

@login_required(login_url=reverse_lazy(settings.LOGIN_URL))
def AddPost(request):
    if(request.method=='POST'):
        form=CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
           post=form.save(commit=False)
           post.user=request.user
           post.save()
        
        print(request.POST.get('allowed_friends'))
        allowed_friends_id=request.POST.get('allowed_friends')

        if allowed_friends_id=="":
                my_friends=get_object_or_404(UserProfile,user=request.user).friends.all()
                for friend in my_friends:
                    post.allowed_friends.add(friend)
        else:
            all_ids=[int(id) for id in allowed_friends_id.split(',') ]
            print(all_ids)
            for id in all_ids:
                user=get_object_or_404(MyUser,pk=id)
                try:
                    post.allowed_friends.add(user)
                except user.DoesNotExist:
                    print("User was not found")
                    response = JsonResponse({'status':'false','success':"not ok"}, status=404)
        response = JsonResponse({'status':'true','success':"ok"}, status=200)
        return response
    else:
        my_friends=get_object_or_404(UserProfile,user=request.user).friends.all()
        print(my_friends)
        form=CreatePostForm()
    return render(request,'AddPost.html',{'allowed_friends':my_friends,'form':form})



def handler404(request, exception, template_name="404.html"):
    response = render(request,template_name)
    response.status_code = 404
    return response

def handler500(request,template_name="500.html"):
    response = render(request,template_name)
    response.status_code = 500
    return response


def handler403(request,template_name="403.html"):
    response = render(request,template_name)
    response.status_code = 403
    return response