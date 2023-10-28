from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    user_created = models.ForeignKey(User, on_delete=models.CASCADE)

    def count_likes(self):
        return Like.objects.filter(post=self).count()
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Logo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    logo = models.ImageField(upload_to='logos/%Y/%m/%d')

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

def return_logo_of_user(user):
    logo = Logo.objects.filter(user=user).first()
    return logo

def users_posts(user):
    posts = Post.objects.filter(user_created = user).all()
    return posts