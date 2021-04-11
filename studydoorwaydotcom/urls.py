
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from .views import home 
from chat.views import getMessages
from rest_framework import routers
from accounts.views import (
	login_view,
	register_view,
	logout_view,
	userprofile_view,
    register_as_teacher_view,
)
router=routers.DefaultRouter()
router.register(r'ajaxusers',getMessages)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classes.urls')),
    path('', include('internetforum.urls')),
    path('', include('quizes.urls',namespace='quizes')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('',home,name='home'),
    path('accounts/login/', login_view,name='login'),
    path('accounts/signup/', register_view,name='signup'),
    path('accounts/logout/', logout_view,name='logout'),
    path('accounts/userprofile/<int:profile_id>', userprofile_view,name='userprofile'),
    path('accounts/register_as_teacher/<int:prof_id>', register_as_teacher_view,name='register_as_teacher'),
    path('chat/', include('chat.urls', namespace='chat')),
    
]
urlpatterns+=router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)