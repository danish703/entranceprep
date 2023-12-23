from django.contrib import admin
from .models import Blog
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','published_at','status']
    list_filter = ['status']

admin.site.register(Blog,BlogAdmin)
