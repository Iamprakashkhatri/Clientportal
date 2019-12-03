
from django import forms

from .models import User,Project,Member

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'username']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email','password']

class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=['title','type',]

class MemberForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Member
        fields = ['address','description','user','project']