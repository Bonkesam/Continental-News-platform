from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords
from django.utils.html import strip_tags

# Create your models here.

# Create the model for category


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Define the model for articles for the blog site
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    preview = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.preview:
            self.preview = truncatewords(strip_tags(self.content), 25)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Create the model for the comments


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
