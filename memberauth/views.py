from .forms import LoginForm
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from client_portal.models import Member,Project
from client_portal.models import User

from django.views import View
from client_portal.models import Comments,Reply
from django.contrib.auth.mixins import PermissionRequiredMixin
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_perms
from django.contrib import messages




class NavView(View):

    def get(self, request):
        content = {}
        user = User.objects.get(username='hari')
        user.backend = 'django.contrib.core.backends.ModelBackend'
        ques_obj = Comments.objects.filter(member__username='hari')
        content['userdetail'] = user
        content['questions'] = ques_obj
        # ans_obj = Reply.objects.filter(comments=ques_obj[:1])
        ans_obj = Reply.objects.filter(user__username='hari')
        content['answers'] = ans_obj
        return render(request, 'memberauth/dashboard.html', content)
        # else:
        #     return redirect(reverse('client_portal:memlist'))


class CommentsLoginView(View):
    # permission_required = ('client_portal.can_add',)
    content = {}
    # content['form'] = LoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommentsLoginView, self).dispatch(request, *args, **kwargs)

    # def get(self, request):
    #     content = {}
    #
    #
    #     if request.user.is_authenticated:
    #         return redirect(reverse('memberauth:dashboard'))
    #     content['form'] = LoginForm
    #     return render(request, 'auth/login.html', content)
    def get(self, request):

        hari = User.objects.get(username='hari')
        # gopal=User.objects.get(username='gopal')
        project = Project.objects.get(title='project1')

        assign_perm('can_view', hari,project)
        # assign_perm('can_view',gopal,project)

        if 'can_view' in get_perms(hari, project):
            return redirect('memberauth:dashboard')
            # return render(request, 'memberauth/dashboard.html', {'{}': {}})


    # def post(self, request):
    #     content = {}
    #     email = request.POST['email']
    #     print(email)
    #     password = request.POST['password']
    #     try:
    #         users =User.objects.filter(email=email)
    #         print(users)
    #         user = authenticate(username=users.first().username, password=password)
    #         print(user)
    #         login(request, user)
    #         return redirect(reverse('memberauth:dashboard'))
    #     except Exception as e:
    #         content = {}
    #         content['form'] = LoginForm
    #         content['error'] = 'Unable to login with provided credentials' + e
    #         return render(request,'memberauth/login.html', content)


class MemberLoginView(View):
    content = {}

    # content['form'] = LoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MemberLoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {}
        content['form'] = LoginForm
        return render(request, 'memberauth/login.html', content)

    def post(self, request):
        content = {}
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        # if email=='hari@gmail.com':
        #     return redirect(reverse('client_portal:list'))
        # else:
        #     return redirect(reverse('client_portal:memlist'))
        # try:
        users =User.objects.filter(email=email)
        print(users )
        user = authenticate(username=users.first().username,password=password)
        login(request, user)
        hari = User.objects.get(username='hari')
        # gopal=User.objects.get(username='gopal')
        project = Project.objects.get(title='project1')

        assign_perm('can_view', hari, project)
        # assign_perm('can_view',gopal,project)

        if 'can_view' in get_perms(hari, project):
            return redirect('client_portal:memlist')
            # return render(request, 'memberauth/dashboard.html', {'{}': {}})
        # except Exception as e:
        #     content = {}
        #     content['form'] = LoginForm
        #     content['error'] = 'Unable to login with provided credentials' + e
        #     return render(request,'memberauth/login.html', content)
        #
