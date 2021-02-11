from django.urls import path
from . import views

urlpatterns = [
	path('classes/create_class/',views.create_class_view,name='create_class'),
	path('classes/class_info/<int:id>/',views.class_info_view,name='class_info'),
	path('classes/s_class_info/<int:id>/',views.s_class_info_view,name='s_class_info'),
	path('classes/class_info/<int:class_id>/<int:assignment_id>/udate',views.update_assignment_view,name='update_assignment'),
	path('classes/class_info/<int:class_id>/<int:assignment_id>/delete',views.delete_assignment_view,name='delete_assignment'),

]