from django.contrib import admin
from .models import Post
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    #show display
    list_display=["title","slug","author","publish","status"]
    #show filter
    list_filter=["status","created"]
    #search field define
    search_fields=["title","body"]
    #auto generate slug based on title
    prepopulated_fields={"slug":("title",)}
    #author field search
    raw_id_fields=["author"]
    date_hierarchy="publish"
    ordering=["status","publish"]