from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from BlogsApp.models import *

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['first_name'].help_text = ''
        self.fields['last_name'].help_text = ''

class LogoForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ['logo']
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'photo', 'is_published']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        self.fields['photo'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
