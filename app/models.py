from django.urls import reverse
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES=[('draft','Draft'),('published','Published')]
    title=models.CharField(max_length=210)
    slug=models.SlugField(max_length=90,unique_for_date='publish') # for user friendly url
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True) # automatically set
    updated=models.DateTimeField(auto_now=True) # automatically  set will it will save last time
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    tags=TaggableManager()
    objects=CustomManager()

    class Meta:
        ordering=('-publish',)
        #for recent one

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])


# For Comment Section
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=32)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return 'Commented By {} on {}'.form(self.name,self.post)
