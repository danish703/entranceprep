from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CourseSerializer,BlogSerializer
from courses.models import Course
from blog.models import Blog
# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class=CourseSerializer
    queryset = Course.objects.filter(status='public')


class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.filter(status='public')
    lookup_field = 'slug'