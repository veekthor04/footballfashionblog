from django.db import models
from solo.models import SingletonModel

# Create your models here.
class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site')
    site_name2 = models.CharField(max_length=255, default='Name')
    slogan = models.CharField(max_length=255, blank=True)
    main_image = models.ImageField(upload_to='post/%Y/%m/%d')
    body1 = models.TextField()
    quote = models.TextField(blank=True)
    body2 = models.TextField(blank=True)
    sub_title = models.CharField(max_length=250, blank=True)
    body3 = models.TextField(blank=True)
    sub_image = models.ImageField(upload_to='post/%Y/%m/%d', blank=True)
    body4 = models.TextField(blank=True)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=250)
    main_image = models.ImageField(upload_to='post/%Y/%m/%d')
    body1 = models.TextField()
    quote = models.TextField(blank=True)
    body2 = models.TextField(blank=True)
    sub_title = models.CharField(max_length=250, blank=True)
    body3 = models.TextField(blank=True)
    sub_image = models.ImageField(upload_to='post/%Y/%m/%d', blank=True)
    body4 = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modifield = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.CharField(max_length=100)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.author
