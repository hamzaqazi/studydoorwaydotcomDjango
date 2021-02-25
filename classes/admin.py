from django.contrib import admin
from .models import *

admin.site.register(ClassRoom)
# admin.site.register(ClassInfo)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Announcement)