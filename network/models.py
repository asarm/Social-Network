from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    follower = models.ForeignKey('User',on_delete=models.CASCADE,related_name='follower')
    target_user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='followee')

class Post(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='author')
    date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField('User',blank=True,related_name='post_likes')
    content = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.pk} - "+self.user.username

    def likes_count(self):
        return self.liked.all.count()

class Like(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)

