from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from .models import *


@login_required
def my_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        logo = LogoForm(request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('my_profile')
        # if logo.is_valid():
        #     logo.save()
        #     messages.success(request, 'Your profile has been updated!')
        #     return redirect('my_profile')
    else:
        form = UserUpdateForm(instance=request.user)
        logo = LogoForm(instance=request.user)
    
    return render(request, 'my_profile.html', {'form': form, 'logo':logo})
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_created = request.user  # Set the user_created field to the current user
            post.save()
            return redirect('post_detail', post_id=post.pk)  # Redirect to the post detail page
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# Edit an existing post
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.user_created:  # Check if the current user is the owner of the post
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post_detail', post_id=post.pk)  # Redirect to the post detail page
        else:
            form = PostForm(instance=post)
        return render(request, 'edit_post.html', {'form': form, 'post': post})
    else:
        # Handle unauthorized access (e.g., show an error message or redirect to an error page)
        return redirect('unauthorized_access_page')
    
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})

def like_post(request, post_id, main):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    x = Like.objects.filter(user=user, post=post).exists()
    if not x:
        like = Like(user=user, post=post)
        like.save()
    else:
        like = Like.objects.filter(user=user, post=post).first()
        like.delete()
    if main==0:
        return redirect('post_detail', post_id=post_id)
    else:
        return redirect('index')

    


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')
