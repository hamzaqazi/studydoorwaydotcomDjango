"""studydoorwaydotcom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
print(router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classes.urls')),
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