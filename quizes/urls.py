from django.urls import path
from .views import(
	QuizListView,
	quiz_view,
	quiz_data_view,
	save_quiz_view,
)

app_name = 'quizes'

urlpatterns = [
	path('quizes_main/',QuizListView.as_view(), name='main-view'),
	path('quizes_main/<pk>/',quiz_view, name='quiz-view'),
	path('quizes_main/<pk>/save/',save_quiz_view, name='save-view'),
	path('quizes_main/<pk>/data/',quiz_data_view, name='quiz-data-view'),
	
]