from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet,BlogViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('blog',BlogViewSet)

urlpatterns = [
    path("", include(router.urls))
]