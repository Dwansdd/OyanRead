from django.db import models
from django.urls import reverse
from django.contrib import admin

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings

class Author(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("author_detail",args=[str(self.id)])


class Articles(models.Model):
    title=models.CharField(max_length=200)
    content = models.TextField(default='')
    image = models.URLField(blank=True, null=True)
    release=models.DateField(blank=True, null=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    source_url = models.URLField(max_length=500,blank=True, null=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("archive_articles",args=[str(self.id)])
    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])
    
