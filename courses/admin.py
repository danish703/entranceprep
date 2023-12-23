from django.contrib import admin
from .models import Course,Subject,TestExam,TestQuestion,OptionImages
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name','slug','status','published_at']
    search_fields = ['course_name',]
    list_filter = ['status',]
admin.site.register(Course,CourseAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_name','slug','status','published_at']
    search_fields = ['subject_name',]
    list_filter = ['status','course']
admin.site.register(Subject,SubjectAdmin)

class TestExamAdmin(admin.ModelAdmin):
    list_display = ['test_name','course','purchased_points','passmarks','status','created_by','created_at']
    search_fields = ['test_name',]
    list_filter =  ['status','course']

admin.site.register(TestExam,TestExamAdmin)

class TesQuestionsAdmin(admin.ModelAdmin):
    list_display = ['question','option1','option2','option3','option4','correctoption','subject','test','created_by']
    search_fields = ['question','subject']
    list_filter = ['subject','test','created_by']

admin.site.register(TestQuestion,TesQuestionsAdmin)
admin.site.register(OptionImages)