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
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('my_profile')
    else:
        logo_user = Logo.objects.filter(user = request.user).first()
        form = UserUpdateForm(instance=request.user)
    return render(request, 'my_profile.html', {'form': form, 'logo':logo_user})
@login_required
def change_logo(request):
    if request.method == 'POST':
        form = LogoForm(request.POST, request.FILES)
        if form.is_valid():
            logo = form.save(commit=False)
            current_logo = Logo.objects.filter(user=request.user).first()
            if current_logo:
                current_logo.delete()
            logo.user = request.user
            logo.save()
            messages.success(request, 'Your Logo has been updated!')
            return redirect('my_profile')
    else:
        form = LogoForm()
    return render(request, 'change_logo.html', {'form': form})

@login_required
def del_logo(request):
    logo = Logo.objects.filter(user=request.user).first()
    logo.delete()
    return redirect('my_profile')

def some_profile(request, username):
    my_profile = True if username == request.user.username else False
    user = User.objects.filter(username=username).first()
    follower_count = user.followers.count()
    following_count = user.following.count()
    logo = return_logo_of_user(user)
    posts = users_posts(user)
    posts_num = len(posts)
    f = Follow.objects.filter(followee=user).select_related('follower')
    followers = []
    for i in f:
        followers.append(i.follower.username)
    follow = False if request.user.username in followers else True
    return render(request, 'some_profile.html', {'user':user, 'logo':logo, 'posts':posts, 'posts_num':posts_num, 'follower':follower_count, 'following':following_count, 'follow':follow, 'my_profile':my_profile})

def follow_user(request, username):
    user_to_follow = User.objects.get(username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, followee=user_to_follow)
    return redirect('some_profile', username=username)

def unfollow_user(request, username):
    user_to_unfollow = User.objects.get(username=username)
    Follow.objects.filter(follower=request.user, followee=user_to_unfollow).delete()
    return redirect('some_profile', username=username)

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
    logos = Logo.objects.all()
    return render(request, 'index.html', {'posts': posts, 'logos':logos})
@login_required
def following_posts(request):
    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower=request.user).values_list('followee', flat=True)
        posts = Post.objects.filter(user_created__in=following_users)
        logos = Logo.objects.all()
        return render(request, 'index.html', {'posts': posts, 'logos': logos})
    else:
        return redirect('index')
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
