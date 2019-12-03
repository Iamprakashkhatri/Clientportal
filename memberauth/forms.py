
from django import forms
from client_portal.models import User
from client_portal.models import Member

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email','password']