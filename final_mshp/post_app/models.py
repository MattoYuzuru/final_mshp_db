from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  
    content = models.TextField()            
    publish_date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)   
    dislikes = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, through='Vote', related_name='voted_posts')

    def __str__(self):
        return self.title
    

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    choice = models.CharField(max_length=10, choices=(('like', 'Like'), ('dislike', 'Dislike')))
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'post']