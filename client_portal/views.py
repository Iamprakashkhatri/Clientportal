from django.shortcuts import render
from django.shortcuts import render,reverse,redirect
from django.urls import reverse_lazy
from .forms import LoginForm,RegisterForm,ProjectForm,MemberForm
from django.views.generic.edit import FormView,View
from .models import Project,Member
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import User
from django.http import Http404

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404



class DashboardView(FormView):


    def get(self, request):
        projects=Project.objects.all()
        return render(request, 'portal/dashboard.html', {'projects':projects})
class RegisterView(FormView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {}
        content['form'] = RegisterForm
        return render(request, 'portal/register.html', content)

    def post(self, request):
        content = {}
        form = RegisterForm(request.POST, request.FILES or None)
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.password = make_password(form.cleaned_data['password'])
            save_it.save()
            # print(save_it)
            # login(request, save_it)
            return redirect(reverse('client_portal:login-view'))
        content['form'] = form
        template = 'portal/register.html'
        return render(request, template, content)



class LoginView(FormView):
    content = {}
    content['form'] = LoginForm
    # member=Member.objects.all()
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)
    def get(self, request):
        return render(request, 'portal/login.html', self.content)

    def post(self, request):
        content = {}
        email = request.POST['email']
        password = request.POST['password']
        try:
            users = User.objects.filter(email=email)
            user = authenticate(request, username=users.first().username, password=password)
            login(request, user)
            return redirect(reverse('client_portal:list'))
        except Exception as e:
            content = {}
            content['form'] = LoginForm
            content['error'] = 'Unable to login with provided credentials' + e
            return render('portal/login.html', content)

class ProjectList(LoginRequiredMixin, ListView):
    model = Project
    # context_object_name = 'items'
    template_name = 'projects/index.html'

class ProjectDetail(UserPassesTestMixin, DetailView):
    model = Project
    # pk_url_kwarg = 'item_id'
    template_name = 'projects/detail.html'

    # context_object_name = 'object_list'
    # queryset = Project.objects.filter(id=[])
    def test_func(self):
        return self.request.user.is_authenticated

    def get_object(self, queryset=None):
        return Member.objects.filter(project__id=self.kwargs['pk'])

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     print(self.object)
    #     context = self.get_context_data(object=self.object)
    #     print(context)
    #     return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['context1'] = self.get_object()
        context['form'] = MemberForm()
        try:
            context['context2'] = Project.objects.get(id=self.kwargs['pk'])
        except Project.DoesNotExist:
            raise Http404
        return context

class ProjectCreation(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create.html'
    success_url = reverse_lazy('client_portal:list')
    # success_message = "Item %(name)s created successfully"
    permission_required = ('client_portal.can_view')

    def get_object(self):
        pk = self.kwargs.get("pk")
        print(pk)
        return get_object_or_404(Project, id=pk)

@method_decorator(login_required, name='dispatch')
class ProjectUpdate(SuccessMessageMixin, UpdateView):
    model = Project
    template_name = 'projects/update.html'
    # pk_url_kwarg = 'item_id'
    form_class = ProjectForm
    success_url = reverse_lazy('client_portal:list')
    # success_message = "Item %(name)s updated successfully"


# @method_decorator(user_passes_test(lambda u: Group.objects.get(name='create store')),name='dispatch')
class ProjectDelete(DeleteView):
    template_name = 'projects/delete.html'
    model = Project
    # pk_url_kwarg = 'item_id'
    success_url = reverse_lazy('client_portal:list')
    # permission_required = ('stor.give_refund',)




class MemberList(LoginRequiredMixin, ListView):
    model = Member
    # context_object_name = 'items'
    template_name = 'members/index.html'


class MemberDetail(UserPassesTestMixin, DetailView):
    model = Member
    # pk_url_kwarg = 'item_id'
    template_name = 'members/detail.html'

    def test_func(self):
        return self.request.user.is_authenticated

def MemberCreate(request):
    # post = Post.objects.all()
    # return render(request,'blog/post_list.html',{'post':post})
    if request.method == 'GET':
        post = User.objects.all()
        return render(request, 'members/create.html', {'post': post})
    if request.method == 'POST':
        form = MemberForm(request.POST)
        print(form)

        if form.is_valid():
            form.save()
        return redirect(request.META['HTTP_REFERER'])


class MemberCreation(SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/create.html'
    success_url = reverse_lazy('client_portal:memlist')
    # def get_object(self, queryset=None):
    #     return Member.objects.filter(project__id=self.kwargs['pk'])
    #
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     print(self.object)
    #     context = self.get_context_data(object=self.object)
    #     print(context)
    #     return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')
class MemberUpdate(SuccessMessageMixin, UpdateView):
    model = Member
    template_name = 'members/update.html'
    # pk_url_kwarg = 'item_id'
    form_class = MemberForm
    success_url = reverse_lazy('client_portal:memlist')
    # success_message = "Item %(name)s updated successfully"


# @method_decorator(user_passes_test(lambda u: Group.objects.get(name='create store')),name='dispatch')
class MemberDelete(DeleteView):
    template_name = 'members/delete.html'
    model = Member
    # pk_url_kwarg = 'item_id'
    success_url = reverse_lazy('client_portal:memlist')
    # permission_required = ('stor.give_refund',)


