from datetime import datetime

from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class Post(models.Model):
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text
