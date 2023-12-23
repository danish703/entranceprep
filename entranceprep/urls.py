from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import SignupView,LoginView,signout,upload_image,deleteImage
urlpatterns = [
    path("",LoginView.as_view(),name="login"),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('signup/', SignupView.as_view(),name='signup'),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', signout,name='signout'),
    path("api/", include('api.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('staff/',include('staff.urls')),
    path('upload_image/',upload_image,name='upload_image'),
    path('delete_image/',deleteImage,name='delete_image'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
