from django.views.generic import View,FormView
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignupForm
from courses.models import OptionImages

class SignupView(FormView):
    template_name = "pages/signup.html"
    form_class = SignupForm
    success_url =  '/login/'

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"Signup Success")
            return redirect('login')
        return render(request,self.template_name,{'form':form})

class LoginView(FormView):
    template_name = 'pages/login.html'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        try:
            User.objects.get(username=username)
        except:
            messages.add_message(request,messages.ERROR,"User with this email is not exist")
            return redirect('login')
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                if user.is_staff:
                    return redirect('staff')
                else:
                    return redirect('dashboard')
            messages.add_message(request,messages.ERROR,"Your accout is not active or blocked")
            return redirect('login')
        else:
            messages.add_message(request,messages.ERROR,"Email and password does not match")
            return redirect('login')


def signout(request):
    logout(request)
    return redirect('login')

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        img = OptionImages(image=uploaded_image)
        try:
            img.save()
            image_url = img.image.url
        except:
            return JsonResponse({'err':'Image can not upload'})
        return JsonResponse({'url': image_url,'id':img.id})
    return JsonResponse({'error': 'No image uploaded.'}, status=400)

@csrf_exempt
def deleteImage(request):
    if request.method=='POST':
        id = request.POST['imgid'];
        try:
            img = OptionImages.objects.get(id=id)
            img.delete()
            return JsonResponse({'msg':'success'})
        except:
            return JsonResponse({'err':'Error occured'})