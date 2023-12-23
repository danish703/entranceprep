from rest_framework import serializers
from courses.models import Course
from blog.models import Blog

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        lookup_field='slug'
        fields ='__all__'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }