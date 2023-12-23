from django.contrib.auth.models import User
from django.db import models
status=(('public','Public'),('draft','Draft'))

class Course(models.Model):
    course_name = models.CharField(max_length=10,verbose_name="Course name")
    image = models.ImageField(upload_to='courses/')
    slug = models.SlugField()
    published_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status,max_length=10,default='draft')

    def __str__(self):
        return self.course_name

    class Meta:
        ordering=['course_name']

class Subject(models.Model):
    subject_name = models.CharField(max_length=100,verbose_name="Subject Name")
    image = models.ImageField(upload_to='subjects/')
    slug = models.SlugField()
    published_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status,max_length=10,default='draft')
    questionTotal = models.PositiveIntegerField(default=20)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name


class TestExam(models.Model):
    test_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30,choices=status,default='draft')
    image = models.ImageField(upload_to='tests/',blank=True,null=True)
    purchased_points = models.PositiveIntegerField(default=10)
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    passmarks = models.PositiveIntegerField(default=40)

    def __str__(self):
        return self.test_name

    class Meta:
        ordering=['-id']


class TestQuestion(models.Model):
    question = models.CharField(verbose_name="Question",help_text="What is the value of PI ?")
    option1 = models.CharField(max_length=250)
    option2 = models.CharField(max_length=250)
    option3 = models.CharField(max_length=250,blank=True,null=True)
    option4 = models.CharField(max_length=250,blank=True,null=True)
    correctoption = models.CharField(max_length=250)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    test = models.ForeignKey(TestExam,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.question


class OptionImages(models.Model):
    image = models.ImageField(upload_to='options/')

    def __str__(self):
        return str(self.image)
