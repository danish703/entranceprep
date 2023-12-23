from django.urls import path
from .views import (
    StaffAdminView,BlogAdminView,TestExamCreateView,TestListView,
    TestUpdateView,TestDeleteView,TestView,questions,questionDelete,CourseView,
    editQuestion,CourseUpdateView,courseDelete)
urlpatterns=[
    path('',StaffAdminView.as_view(),name='staff'),
    path('blogs/',BlogAdminView.as_view(),name='admin_blog'),
    path('courses/',CourseView.as_view(),name='course_admin'),
    path('courses/update/<int:pk>',CourseUpdateView.as_view(),name='course_update'),
    path('courses/delete/<int:id>/', courseDelete, name='course_delete'),
    path('tests/create',TestExamCreateView.as_view(),name='test_create'),
    path('tests/',TestListView.as_view(),name='tests'),
    path('tests/edit/<int:pk>',TestUpdateView.as_view(),name='test_update'),
    path('tests/delete/<int:pk>',TestDeleteView.as_view(),name='test_delete'),
    path('tests/<int:pk>',TestView.as_view(),name='test'),
    path('tests/<int:testId>/<slug:subject_slug>',questions,name='questions'),
    path('question/delete/<int:id>/',questionDelete,name='question_delete'),
    path('question/edit/<int:id>/',editQuestion,name='question_edit'),
]