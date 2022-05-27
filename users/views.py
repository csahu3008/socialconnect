import email
from django.shortcuts import render,redirect,HttpResponse,reverse,get_object_or_404
from django.contrib.auth import login,authenticate
from django.views.generic import FormView
from .models import MyUser,UserProfile
from .forms import MyUserForm,loginform
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.db.models.query import F,Q
from django.http import JsonResponse

# Create your views here.
def signup(request):
    if(request.method=='POST'):
        form=MyUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()
            user.save()
            cd=form.cleaned_data['name']
            request.session['cookie']=cd
            context={'form':form,'cook':request.session.get('cookie','hello')}
            return render(request,'registration/signup_done.html',context)
        
    else:
        form=MyUserForm()
    return render(request,'registration/signup.html',{'form':form})


def Login(request):
    if request.session.get('mobile') or request.session.get('email'):
        return redirect(reverse('feed'))
    else:
        if request.method=='POST':
            form=loginform(request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                mobile=form.cleaned_data['mobile']
                user=authenticate(request,mobile=mobile,email=email,password=password)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        request.session['email']=email
                        request.session['mobile']=mobile
                        return redirect(reverse('feed'))
                    else:
                        return HttpResponse('you are not active user')
                else:
                    return HttpResponse('Your account is not found')
            else:
                return HttpResponse('your login details are invalid')
        else:
            form=loginform()
        return render(request,'registration/login.html',{'form':form})

class SeeUsers(TemplateView):
    template_name='search_users.html'


    def get(self, request, *args, **kwargs):

        if self.request.GET and self.request.user.is_anonymous:
            qs=self.request.GET.get('q')
            filtered_users=MyUser.objects.all().filter(Q(name__contains=qs) | Q(email__iexact=qs) | Q(mobile__iexact=qs))
            strangers=[]
            strangers.extend(filtered_users)
            context={
                'strangers':strangers,
                'query':qs
            }
            return render(request, 'search_users.html',context)
       
        elif self.request.GET and self.request.user.is_authenticated:
            qs=self.request.GET.get('q')
            # print(MyUser.objects.all().filter(name__contains=qs))
            filtered_users=MyUser.objects.all().filter(Q(name__contains=qs) | Q(email__iexact=qs) | Q(mobile__iexact=qs))
            my_friends=UserProfile.objects.all().get(user=self.request.user).friends.all().filter(Q(name__contains=qs) | Q(email__iexact=qs) | Q(mobile__iexact=qs))
            common_friends=list(filtered_users & my_friends)
            strangers=[]
            first_set=filtered_users.difference(my_friends)
            strangers.extend(first_set)        #first set difference
            # strangers.remove(self.request.user) #remove current user
            print(strangers)
            context={
                'my_friends':my_friends,
                'strangers':strangers,
                'query':qs
            }
            return render(request, 'search_users.html',context)

        return render(request, 'search_users.html',{})
        

class AddUserAsFriend(TemplateView):
    def post(self, request, *args, **kwargs):
        print(self.request.POST.get('id'))
        stranger=get_object_or_404(MyUser,pk=self.request.POST.get('id'))
        try:
            print("User is ",stranger)
            my_profile=get_object_or_404(UserProfile,user=self.request.user)
            # add stranger 
            if stranger not in my_profile.friends.all():
                my_profile.friends.add(stranger)
            response = JsonResponse({'status':'true','success':"ok"}, status=200)
        except stranger.DoesNotExist:
            response = JsonResponse({'status':'false','success':"not ok"}, status=404)
            
        return response


class ShowUserProfile(DetailView):
    template_name='ShowProfile.html'
    model=MyUser
    context_object_name='user'
    def get_context_data(self, **kwargs):
        my_friends=get_object_or_404(UserProfile,user=self.request.user).friends.all()
        print(my_friends)

        user_friends=get_object_or_404(UserProfile,user=self.get_object()).friends.all()
        print(user_friends)

        mutual_friends=my_friends & user_friends

        kwargs['mutual_friends']=mutual_friends
        return super().get_context_data(**kwargs)