import os
from pathlib import Path
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView,DetailView
from django.shortcuts import render,redirect
from blog.models import Blog
from courses.models import Course
from .forms import TestCreateForm,CourseForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from courses.models import TestExam,Subject,TestQuestion
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
class StaffAdminView(LoginRequiredMixin,TemplateView):
    login_url = 'login'
    template_name = 'staff/dashboard.html'

    def get(self,request):
        return render(request,self.template_name)


class BlogAdminView(LoginRequiredMixin,ListView):
    login_url = 'login'
    template_name = 'staff/Blogs.html'
    model = Blog

class CourseView(LoginRequiredMixin,CreateView):
    login_url = 'login'
    template_name = 'staff/courses.html'
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_admin')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Saved successfully")
        return super(CourseView,self).form_valid(form)

class CourseUpdateView(LoginRequiredMixin,UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'staff/course_edit.html'
    success_url = reverse_lazy("course_admin")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Updated successfully")
        return super(CourseUpdateView,self).form_valid(form)


class TestExamCreateView(LoginRequiredMixin,CreateView):
    login_url = 'login'
    form_class = TestCreateForm
    template_name = 'staff/test_create.html'
    success_url = reverse_lazy('test_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_tests'] = TestExam.objects.all()[:5]
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Saved successfully")
        return super(TestExamCreateView,self).form_valid(form)


class TestListView(LoginRequiredMixin,ListView):
    login_url = 'login'
    template_name = 'staff/tests.html'
    model = TestExam



class TestUpdateView(LoginRequiredMixin,UpdateView):
    model = TestExam
    form_class = TestCreateForm
    template_name = 'staff/edit_test.html'
    success_url =  reverse_lazy("tests")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_tests'] = TestExam.objects.all().order_by('-id')[:5]
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Updated successfully")
        return super(TestUpdateView,self).form_valid(form)


class TestDeleteView(LoginRequiredMixin,DeleteView):
    model =  TestExam
    success_url = reverse_lazy("tests")
    permission_denied_message = "You do not have permission to delete"
    template_name = "staff/test_delete.html"

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Deleted successfully")
        return super(TestDeleteView,self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.add_message(request,messages.ERROR,"Permission denied")
            return redirect('tests')
        else:
            super(TestDeleteView,self).post(request,*args,**kwargs)
            return redirect('tests')


class TestView(LoginRequiredMixin,DetailView):
    model = TestExam
    template_name = 'staff/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.filter(course=self.object.course)
        context["subject_details"] = subjects
        context["questions"] = TestQuestion.objects.filter(test=self.object)
        return context

@login_required(login_url='login')
def questions(request,testId,subject_slug):
    context = {}
    test = TestExam.objects.get(pk=testId)
    context["test"] = test
    subject = Subject.objects.get(slug=subject_slug)
    context["subject"] = subject
    questions = TestQuestion.objects.filter(test=test,subject=subject)
    no_of_questions = len(questions)
    context["questions"] = questions
    response = dict()
    if request.method=="GET":
        return render(request,'staff/questions.html',context)
    else:
        question = request.POST['question']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        correctoption = request.POST['correct']
        testQuestion = TestQuestion(question=question,option1=option1,
                                    option2=option2,option3=option3,
                                    option4=option4,
                                    correctoption=correctoption,test=test,subject=subject,created_by=request.user)
        if no_of_questions<subject.questionTotal:
            try:
                testQuestion.save()
                messages.add_message(request,messages.SUCCESS,"New Question added")
                response['success'] = "success"
                return JsonResponse(response)
            except Exception as e:
                response["error"] = str(e)
                return JsonResponse(response)
        else:
            response['error'] = "Exceed the Question Limit"
            return JsonResponse(response)


@login_required(login_url='login')
def editQuestion(request,id):
    question = TestQuestion.objects.get(pk=id)
    if request.method == 'GET':
        context = {'question':question}
        return render(request,'staff/edit_question.html',context)
    else:
        question = TestQuestion.objects.get(id=request.POST["qid"])
        question.question = request.POST["question"]
        question.option1 = request.POST["option1"]
        question.option2 = request.POST["option2"]
        question.option3 = request.POST["option3"]
        question.option4 = request.POST["option4"]
        question.correctoption = request.POST["correct"]
        question.save()
        return redirect('questions', question.test.id, question.subject.slug)

def questionDelete(request,id):
    if request.user.is_staff:
        try:
            question = TestQuestion.objects.get(id=id)
            subslug = question.subject.slug
            test = question.test.id
            if question.option1.startswith("/media"):
                file_path = str(settings.BASE_DIR)+question.option1
                if os.path.exists(file_path):
                    os.remove(file_path)
            if question.option2.startswith("/media"):
                file_path = str(settings.BASE_DIR) + question.option2
                if os.path.exists(file_path):
                    os.remove(file_path)
            if question.option3.startswith("/media"):
                file_path = str(settings.BASE_DIR) + question.option3
                if os.path.exists(file_path):
                    os.remove(file_path)
            if question.option4.startswith("/media"):
                file_path = str(settings.BASE_DIR) + question.option4
                if os.path.exists(file_path):
                    os.remove(file_path)
            question.delete()
            messages.add_message(request,messages.SUCCESS,"Deleted successfully")
            return redirect("questions",test,subslug)
        except Exception as e:
            messages.add_message(request,messages.ERROR,str(e))
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.add_message(request,messages.ERROR,"You do not have permission")
        return redirect('login')

def courseDelete(request,id):
    if request.user.is_staff:
        try:
            course = Course.objects.get(id=id)
            course.delete()
            messages.add_message(request,messages.SUCCESS,"Deleted successfully")
            return redirect("course_admin")
        except Exception as e:
            messages.add_message(request,messages.ERROR,str(e))
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.add_message(request,messages.ERROR,"You do not have permission")
        return redirect('login')