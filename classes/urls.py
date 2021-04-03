from django.urls import path
from . import views

urlpatterns = [
	path('classes/create_class/',views.create_class_view,name='create_class'),
	path('classes/class_info/<int:id>/',views.class_info_view,name='class_info'),
	path('classes/s_class_info/<int:id>/',views.s_class_info_view,name='s_class_info'),
	path('classes/s_class_info/<int:class_id>/<int:assignment_id>/details',views.s_assignment_detail_view,name='s_assignment_detail'),
	path('classes/class_info/<int:class_id>/<int:assignment_id>/update',views.update_assignment_view,name='update_assignment'),
	path('classes/class_info/<int:class_id>/<int:assignment_id>/delete',views.delete_assignment_view,name='delete_assignment'),
	path('classes/like/<int:pk>/<int:class_id>',views.announcement_likes_view,name='announcement_likes'),
	path('classes/comment/<int:announcement_id>/<int:class_id>',views.announcement_comments_view,name='announcement_comments'),
	path('classes/<int:class_id>/student_work',views.student_work_view,name='student_work'),
	path('classes/notification/<int:notification_id>/',views.delete_notification_view,name='delete_notification'),
	# path('classes/s_class_info/<int:id>/<int:assignment_id>',views.submit_assignment_view,name='submit_assignment'),

]