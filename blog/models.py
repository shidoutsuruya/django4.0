from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
# many to one  relationship
from django.contrib.auth.models import User
#create url reverse
from django.urls import reverse
#create taggit
from taggit.managers import TaggableManager
#Create model managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
# Create your models here.
class Post(models.Model):
    #add manager
    objects=models.Manager()
    published=PublishedManager()
    #adding a status field
    class Status(models.TextChoices):
        DRAFT="DF","Draft"
        PUBLISHED="PB","PubliPosshed"
    #add many to one
    author=models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="blog_posts")
    #create model
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250,unique_for_date="publish")
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2,
                            choices=Status.choices,
                            default=Status.DRAFT)
    #taggit
    tags=TaggableManager()
    #default sort order
    class Meta:
        ordering=['-publish']
        indexes=[
            models.Index(fields=["-publish"]),
        ]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blog:post_detail",args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])
#create model of comments
class Comment(models.Model):
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    name=models.CharField(max_length=80)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=["created"]
        indexes=[
            models.Index(fields=["created"]),
        ]
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"